"""Étape 7 — Logique d'import WordPress (nettoyage HTML, création des objets).

Utilisée par les commandes ``wordpress_audit``, ``wordpress_import`` et
``wordpress_report``. Aucune donnée n'est inventée : chaque élément est
importé en brouillon (ou publié avec ``--publish``), en attente de la
validation humaine exigée par le cahier des charges (§7, §30).
"""

import hashlib
import html as html_module
import re
import urllib.parse
from datetime import datetime
from html.parser import HTMLParser

from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify

from apps.articles.models import Article, ArticleCategory, ArticleTag
from apps.media.models import MediaCategory, MediaItem
from apps.migration import wp_api
from apps.migration.models import ImportedRecord, URLMapping
from apps.pages.models import Page

# --- Nettoyage HTML ---------------------------------------------------------

ALLOWED_TAGS = {
    "a", "b", "blockquote", "br", "code", "div", "em", "figcaption", "figure",
    "h1", "h2", "h3", "h4", "h5", "h6", "hr", "i", "img", "li", "ol", "p",
    "pre", "span", "strong", "table", "tbody", "td", "th", "thead", "tr", "u", "ul",
}
ALLOWED_ATTRS = {
    "a": {"href", "title", "target", "rel"},
    "img": {"src", "alt", "width", "height"},
    "td": {"colspan", "rowspan"},
    "th": {"colspan", "rowspan"},
}
VOID_TAGS = {"br", "hr", "img"}
DANGEROUS_SCHEMES = ("javascript:", "vbscript:", "data:", "file:")

_IMAGE_RE = re.compile(
    r"https?://[^\s\"'<>]+?\.(?:jpe?g|png|gif|webp|avif|bmp)(?:\?[^\s\"'<>]*)?",
    re.IGNORECASE,
)
_SKIP_TAG_NAMES = {"AU", "dailyprompt", "dailyprompt-1958"}
_POST_256_TITLE = "Lutte contre la malnutrition des enfants de moins de 10 ans — Nyiragongo"


def clean_media_url(url: str) -> str:
    """Normalise une URL d'image WordPress : absolue, sans paramètres de taille (?w=…)."""
    url = (url or "").strip()
    if not url:
        return ""
    parsed = urllib.parse.urlparse(url)
    if not parsed.scheme:
        parsed = urllib.parse.urlparse(urllib.parse.urljoin(wp_api.SITE_URL + "/", url))
    if parsed.scheme.lower() in DANGEROUS_SCHEMES:
        return ""
    return urllib.parse.urlunparse(parsed._replace(query=""))


def _clean_attrs(tag: str, attrs: list, image_map: dict) -> list:
    allowed = ALLOWED_ATTRS.get(tag, set())
    cleaned = []
    for key, value in attrs:
        key = key.lower()
        if key not in allowed:
            continue
        value = (value or "").strip()
        if key in ("src", "href"):
            if value.lower().startswith(DANGEROUS_SCHEMES):
                continue
            if key == "src":
                value = clean_media_url(value)
                value = image_map.get(value, value)
        cleaned.append((key, value))
    return cleaned


class _Sanitizer(HTMLParser):
    """Conserve uniquement les balises/attributs autorisés et réécrit les images."""

    def __init__(self, image_map: dict | None = None):
        super().__init__(convert_charrefs=True)
        self.image_map = image_map or {}
        self.parts = []

    def handle_starttag(self, tag, attrs):
        tag = tag.lower()
        if tag not in ALLOWED_TAGS:
            return
        cleaned = _clean_attrs(tag, attrs, self.image_map)
        self.parts.append(f"<{tag}" + self._attrs_str(cleaned) + ("" if tag in VOID_TAGS else ">"))

    def handle_startendtag(self, tag, attrs):
        tag = tag.lower()
        if tag not in ALLOWED_TAGS:
            return
        cleaned = _clean_attrs(tag, attrs, self.image_map)
        self.parts.append(f"<{tag}" + self._attrs_str(cleaned) + "/>")

    def handle_endtag(self, tag):
        tag = tag.lower()
        if tag in ALLOWED_TAGS and tag not in VOID_TAGS:
            self.parts.append(f"</{tag}>")

    def handle_data(self, data):
        self.parts.append(data)

    @staticmethod
    def _attrs_str(attrs: list) -> str:
        if not attrs:
            return ""
        return "".join(f' {k}="{v.replace("&", "&amp;").replace('"', "&quot;")}"' for k, v in attrs)


def sanitize_html(raw: str, image_map: dict | None = None) -> str:
    """Nettoie le HTML WordPress : balises autorisées uniquement, URLs d'images réécrites."""
    if not raw:
        return ""
    parser = _Sanitizer(image_map)
    try:
        parser.feed(raw)
        parser.close()
    except Exception:
        return ""
    return "".join(parser.parts)


def strip_tags(raw: str) -> str:
    """Extrait le texte brut d'un fragment HTML (pour l'extrait)."""
    return re.sub(r"<[^>]*>", " ", raw or "")


def image_urls_from_html(content: str) -> set[str]:
    """Ensemble des URLs d'images présentes dans un contenu WordPress."""
    return {clean_media_url(m) for m in _IMAGE_RE.findall(content or "") if clean_media_url(m)}


# --- Médias -----------------------------------------------------------------


def get_or_create_media(url: str, subdir: str = "wp") -> MediaItem | None:
    """Télécharge une image, la déduplique (SHA-256) et crée un MediaItem.

    Retourne None si le téléchargement échoue (l'URL source est alors
    conservée dans le contenu HTML, et l'écart est tracé dans le rapport).
    """
    clean = clean_media_url(url)
    if not clean:
        return None
    existing = MediaItem.objects.filter(source_url=clean).first()
    if existing:
        return existing
    try:
        data, name = wp_api.download_file(clean)
    except wp_api.WordPressAPIError:
        return None
    checksum = hashlib.sha256(data).hexdigest()
    existing = MediaItem.objects.filter(checksum=checksum).first()
    if existing:
        if not existing.source_url:
            existing.source_url = clean
            existing.save(update_fields=["source_url"])
        return existing
    safe_name = re.sub(r"[^A-Za-z0-9._-]+", "-", name).strip("-") or "image.jpg"
    now = timezone.now()
    category, _ = MediaCategory.objects.get_or_create(
        slug="import-wordpress", defaults={"name": "Import WordPress"}
    )
    item = MediaItem(
        file=ContentFile(data, name=f"wp/{now:%Y/%m}/{safe_name}"),
        kind="image",
        title=safe_name.rsplit(".", 1)[0],
        checksum=checksum,
        source_url=clean,
        category=category,
    )
    item.save()
    return item


# --- Traçabilité ------------------------------------------------------------


def log_record(
    run,
    source_type: str,
    source_id: str,
    source_title: str,
    source_url: str,
    dest_model: str,
    dest_id: int | None,
    status: str,
    notes: str = "",
) -> str:
    """Crée un ImportedRecord et retourne une ligne de résumé pour la console."""
    ImportedRecord.objects.update_or_create(
        run=run,
        source_type=source_type,
        source_id=source_id or "?",
        defaults={
            "source_title": source_title[:300],
            "source_url": source_url[:500],
            "destination_model": dest_model or "",
            "destination_id": dest_id,
            "status": status,
            "notes": notes[:2000],
        },
    )
    return f"[{status}] {source_type} {source_id or '?'} : {source_title} {notes}"


def map_old_to_new(old_url: str, new_url: str) -> None:
    """Enregistre la correspondance ancienne URL WordPress → nouvelle URL Django."""
    if not old_url:
        return
    URLMapping.objects.update_or_create(old_url=old_url, defaults={"new_url": new_url})


# --- Import -----------------------------------------------------------------


def _parse_date(value) -> datetime:
    if not value:
        return timezone.now()
    try:
        parsed = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    except ValueError:
        return timezone.now()
    if timezone.is_naive(parsed):
        parsed = timezone.make_aware(parsed)
    return parsed


def _resolve_author():
    User = get_user_model()
    return (
        User.objects.filter(is_superuser=True).order_by("id").first()
        or User.objects.order_by("id").first()
    )


def import_category(raw: dict) -> ArticleCategory | None:
    name = (raw.get("name") or "").strip()
    if not name:
        return None
    slug = (raw.get("slug") or slugify(name))[:240]
    category, _ = ArticleCategory.objects.get_or_create(slug=slug, defaults={"name": name})
    return category


def import_tag(raw: dict) -> ArticleTag | None:
    name = (raw.get("name") or "").strip()
    if not name or name in _SKIP_TAG_NAMES:
        return None
    slug = (raw.get("slug") or slugify(name))[:240]
    tag, _ = ArticleTag.objects.get_or_create(slug=slug, defaults={"name": name})
    return tag


def _items_from(raw) -> list:
    if isinstance(raw, dict):
        return list(raw.values())
    return list(raw or [])


def import_post(run, raw: dict, author=None, publish=False, download_media=True, force=False) -> str:
    wp_id = str(raw.get("ID") or "").strip()
    source_url = (raw.get("URL") or "").strip()
    title = html_module.unescape((raw.get("title") or "").strip())
    if not wp_id or not title:
        return log_record(run, "post", wp_id, title or "(sans titre)", source_url,
                          None, None, "ERROR", "Titre ou ID manquant")

    notes = []
    if wp_id == "256" and len(title) > 300:
        # Anomalie connue (audit §3/§10) : texte complet collé dans le titre.
        title = _POST_256_TITLE
        notes.append("Titre restructuré depuis le contenu (anomalie WP post 256) — à valider")

    slug = (raw.get("slug") or "").strip()
    if not slug or len(slug) > 200:
        slug = slugify(title)
    slug = slug[:240] or f"post-{wp_id}"
    if Article.objects.filter(slug=slug).exists() and not force:
        return log_record(run, "post", wp_id, title, source_url,
                          "articles.Article", None, "SKIPPED", "Slug déjà utilisé")

    raw_content = raw.get("content") or ""
    image_map = {}
    if download_media:
        for url in sorted(image_urls_from_html(raw_content)):
            item = get_or_create_media(url, subdir=f"wp/{wp_id}")
            if item:
                image_map[url] = item.file.url

    article = Article(
        slug=slug,
        title=title,
        excerpt=strip_tags(raw.get("excerpt") or "")[:500],
        content=sanitize_html(raw_content, image_map=image_map),
        status="published" if publish else "draft",
        published_at=_parse_date(raw.get("date")),
        canonical_url=source_url,
        author=author,
        publication_authorized=bool(publish),
    )
    article.save()

    featured = (raw.get("featured_image") or "").strip()
    if not featured:
        thumbnail = raw.get("post_thumbnail") or {}
        featured = (thumbnail.get("URL") or thumbnail.get("url") or "").strip()
    if featured and download_media:
        item = get_or_create_media(featured, subdir=f"wp/{wp_id}")
        if item:
            article.cover_image = item
            article.save(update_fields=["cover_image"])

    for item in _items_from(raw.get("categories")):
        category = import_category(item)
        if category:
            article.categories.add(category)
    for item in _items_from(raw.get("tags")):
        tag = import_tag(item)
        if tag:
            article.tags.add(tag)

    map_old_to_new(source_url, reverse("articles:detail", kwargs={"slug": article.slug}))
    return log_record(run, "post", wp_id, title, source_url,
                      "articles.Article", article.pk, "IMPORTED", "; ".join(notes))


def import_page(run, raw: dict, publish=False, download_media=True, force=False) -> str:
    wp_id = str(raw.get("ID") or "").strip()
    source_url = (raw.get("URL") or "").strip()
    title = html_module.unescape((raw.get("title") or "").strip())

    if wp_id == "177":
        return log_record(run, "page", wp_id, title or "MANASSE WEDDING", source_url,
                          None, None, "SKIPPED", "Contenu personnel (MANASSE WEDDING) — hors périmètre")
    if not wp_id or not title:
        return log_record(run, "page", wp_id, title or "(sans titre)", source_url,
                          None, None, "ERROR", "Titre ou ID manquant")

    slug = (raw.get("slug") or "").strip()
    if not slug or len(slug) > 200:
        slug = slugify(title)
    slug = slug[:240] or f"page-{wp_id}"
    if Page.objects.filter(slug=slug).exists() and not force:
        return log_record(run, "page", wp_id, title, source_url,
                          "pages.Page", None, "SKIPPED", "Slug déjà utilisé")

    raw_content = raw.get("content") or ""
    image_map = {}
    if download_media:
        for url in sorted(image_urls_from_html(raw_content)):
            item = get_or_create_media(url, subdir=f"wp/page-{wp_id}")
            if item:
                image_map[url] = item.file.url

    page = Page(
        slug=slug,
        title=title,
        content=sanitize_html(raw_content, image_map=image_map),
        status="published" if publish else "draft",
        in_menu=False,
    )
    page.save()

    map_old_to_new(source_url, reverse("pages:page_detail", kwargs={"slug": page.slug}))
    return log_record(run, "page", wp_id, title, source_url,
                      "pages.Page", page.pk, "IMPORTED", "")
