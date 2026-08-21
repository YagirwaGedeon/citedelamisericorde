"""Client minimal de l'API publique WordPress.com (§7, §19).

Stdlib uniquement (urllib) — aucune dépendance externe requise.
L'API REST WordPress native (``/wp-json/``) répond 404 sur ce site
WordPress.com ; l'API publique ``public-api.wordpress.com`` fonctionne
sans jeton pour les données publiques (posts, pages, catégories, tags).

Les identifiants WordPress, s'ils sont fournis via l'environnement
(``WORDPRESS_USERNAME`` / ``WORDPRESS_PASSWORD``), ne sont jamais
journalisés ni affichés.
"""

import base64
import json
import urllib.error
import urllib.parse
import urllib.request

from django.conf import settings

API_BASE = (
    getattr(settings, "WORDPRESS_API_BASE", "")
    .strip()
    .rstrip("/")
    or "https://public-api.wordpress.com/rest/v1.1/sites/citedelamisericorde.wordpress.com"
)
SITE_URL = (
    getattr(settings, "WORDPRESS_SITE", "https://citedelamisericorde.wordpress.com")
    .strip()
    .rstrip("/")
)
TIMEOUT = 30
USER_AGENT = "Cite-de-la-Misericorde-Migration/1.0"


class WordPressAPIError(RuntimeError):
    """Erreur d'appel à l'API WordPress.com (HTTP, réseau ou format)."""


def _auth_headers() -> dict:
    user = getattr(settings, "WORDPRESS_USERNAME", "")
    password = getattr(settings, "WORDPRESS_PASSWORD", "")
    if user and password:
        token = base64.b64encode(f"{user}:{password}".encode("utf-8")).decode("ascii")
        return {"Authorization": f"Basic {token}"}
    return {}


def wp_get(
    resource: str = "",
    params: dict | None = None,
    timeout: int = TIMEOUT,
    base: str | None = None,
) -> dict | list:
    """GET JSON sur l'API WordPress.com ; lève WordPressAPIError en cas d'échec."""
    url = f"{(base or API_BASE)}/{resource.lstrip('/')}"
    if params:
        query = {k: v for k, v in params.items() if v is not None}
        if query:
            url += "?" + urllib.parse.urlencode(query)
    request = urllib.request.Request(
        url, headers={"User-Agent": USER_AGENT, **_auth_headers()}
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        raise WordPressAPIError(f"HTTP {exc.code} sur {url}") from exc
    except urllib.error.URLError as exc:
        raise WordPressAPIError(f"Erreur réseau sur {url} : {exc.reason}") from exc
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        raise WordPressAPIError(f"Réponse JSON invalide sur {url}") from exc


def fetch_collection(
    resource: str, params: dict | None = None, number: int = 50, base: str | None = None
) -> list:
    """Parcours paginé d'une collection publique (posts, pages, categories, tags…).

    Retourne la liste plate des éléments bruts tels que renvoyés par l'API v1.1.
    """
    params = dict(params or {})
    params.setdefault("number", min(number, 100))
    page, items = 1, []
    while True:
        data = wp_get(resource, {**params, "page": page}, base=base)
        if isinstance(data, dict):
            batch = None
            for key in ("posts", "pages", "categories", "tags", "media"):
                value = data.get(key)
                if value is not None:
                    batch = list(value.values()) if isinstance(value, dict) else list(value)
                    break
            batch = batch or []
        elif isinstance(data, list):
            batch = data
        else:
            raise WordPressAPIError(f"Format inattendu pour {resource}")
        items.extend(batch)
        found = data.get("found", 0) if isinstance(data, dict) else 0
        if not batch or (found and len(items) >= found):
            break
        page += 1
    return items


def fetch_pages() -> list:
    """Pages du site WordPress.

    L'endpoint ``/pages`` de l'API v1.1 répond 404 sur ce site : les pages
    sont récupérées via l'API v1 ``/posts?type=page`` (mêmes champs).
    """
    info = wp_get("")
    site_key = info.get("ID") or API_BASE.rstrip("/").rsplit("/", 1)[-1]
    v1_base = f"https://public-api.wordpress.com/rest/v1/sites/{site_key}"
    return fetch_collection("posts", {"type": "page"}, base=v1_base)


def download_file(url: str, timeout: int = TIMEOUT) -> tuple[bytes, str]:
    """Télécharge un fichier (image WordPress) ; retourne (contenu, nom du fichier)."""
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            data = response.read()
    except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError) as exc:
        raise WordPressAPIError(f"Téléchargement impossible : {url}") from exc
    name = urllib.parse.urlparse(url).path.rsplit("/", 1)[-1] or "fichier.bin"
    return data, name
