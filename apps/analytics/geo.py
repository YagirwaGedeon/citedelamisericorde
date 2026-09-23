"""Détection de pays privacy-friendly (Accept-Language, puis GeoIP2 si dispo)."""

from __future__ import annotations

import logging

logger = logging.getLogger(__name__)

# Région ISO ( Accept-Language xx-YY ) → nom français (couverture utile Afrique + monde)
_REGION_TO_COUNTRY = {
    "CD": "RD Congo",
    "CG": "Congo-Brazzaville",
    "BI": "Burundi",
    "RW": "Rwanda",
    "UG": "Ouganda",
    "KE": "Kenya",
    "TZ": "Tanzanie",
    "ZM": "Zambie",
    "ZW": "Zimbabwe",
    "AO": "Angola",
    "MZ": "Mozambique",
    "MW": "Malawi",
    "SD": "Soudan",
    "SS": "Soudan du Sud",
    "ET": "Éthiopie",
    "NG": "Nigéria",
    "GH": "Ghana",
    "CI": "Côte d’Ivoire",
    "SN": "Sénégal",
    "CM": "Cameroun",
    "GA": "Gabon",
    "TG": "Togo",
    "BJ": "Bénin",
    "BF": "Burkina Faso",
    "ML": "Mali",
    "NE": "Niger",
    "TD": "Tchad",
    "MG": "Madagascar",
    "MU": "Maurice",
    "ZA": "Afrique du Sud",
    "EG": "Égypte",
    "MA": "Maroc",
    "DZ": "Algérie",
    "TN": "Tunisie",
    "LY": "Libye",
    "FR": "France",
    "BE": "Belgique",
    "CH": "Suisse",
    "CA": "Canada",
    "US": "États-Unis",
    "GB": "Royaume-Uni",
    "DE": "Allemagne",
    "ES": "Espagne",
    "IT": "Italie",
    "PT": "Portugal",
    "NL": "Pays-Bas",
    "LU": "Luxembourg",
    "BR": "Brésil",
    "IN": "Inde",
    "CN": "Chine",
    "JP": "Japon",
    "AU": "Australie",
    "RU": "Russie",
    "TR": "Turquie",
    "SA": "Arabie saoudite",
    "AE": "Émirats arabes unis",
    "IL": "Israël",
    "PK": "Pakistan",
    "BD": "Bangladesh",
    "PH": "Philippines",
    "ID": "Indonésie",
    "KR": "Corée du Sud",
    "MX": "Mexique",
    "AR": "Argentine",
    "CL": "Chile",
    "CO": "Colombie",
    "PE": "Pérou",
    "VE": "Venezuela",
    "SE": "Suède",
    "NO": "Norvège",
    "DK": "Danemark",
    "FI": "Finlande",
    "PL": "Pologne",
    "CZ": "Tchéquie",
    "AT": "Autriche",
    "IE": "Irlande",
    "GR": "Grèce",
    "RO": "Roumanie",
    "UA": "Ukraine",
}

# Langues seules (sans région) → pays le plus probable / libellé générique
_LANG_TO_COUNTRY = {
    "fr": "France",
    "en": "International",
    "sw": "Afrique de l’Est",
    "pt": "Portugal / Brésil",
    "es": "Espagne / Amérique latine",
    "de": "Allemagne",
    "ar": "Monde arabe",
    "zh": "Chine",
    "ru": "Russie",
    "ja": "Japon",
}


def country_from_accept_language(header: str | None) -> str:
    """Extrait un pays depuis Accept-Language (ex: fr-CD,fr;q=0.9 → RD Congo)."""
    if not header:
        return ""
    # priorité : première entrée avec région
    for part in header.split(","):
        lang = part.split(";")[0].strip().lower()
        if not lang or lang == "*":
            continue
        if "-" in lang:
            region = lang.split("-", 1)[1].upper()
            # en-r GB special-case
            if region in ("GB", "UK"):
                return _REGION_TO_COUNTRY["GB"]
            name = _REGION_TO_COUNTRY.get(region)
            if name:
                return name
        else:
            # mémoriser langue pure comme fallback
            pass
    # fallback : première langue pure
    first = header.split(",")[0].split(";")[0].strip().lower().split("-")[0]
    return _LANG_TO_COUNTRY.get(first, "")


_geoip_reader = None
_geoip_tried = False


def _get_geoip():
    global _geoip_reader, _geoip_tried
    if _geoip_tried:
        return _geoip_reader
    _geoip_tried = True
    try:
        import os

        from django.conf import settings

        city = getattr(settings, "GEOIP_CITY", "") or os.environ.get("GEOIP_CITY", "")
        country_db = getattr(settings, "GEOIP_COUNTRY", "") or os.environ.get("GEOIP_COUNTRY", "")
        path = city or country_db
        if not path:
            return None
        if city and os.path.exists(city):
            from geoip2.database import Reader

            _geoip_reader = Reader(city)
        elif country_db and os.path.exists(country_db):
            from geoip2.database import Reader

            _geoip_reader = Reader(country_db)
    except Exception as exc:  # noqa: BLE001 — GeoIP optionnel
        logger.debug("GeoIP indisponible: %s", exc)
        _geoip_reader = None
    return _geoip_reader


def country_from_ip(ip: str) -> str:
    """GeoIP2 si configuré, sinon chaîne vide."""
    if not ip or ip in ("unknown", "127.0.0.1", "::1"):
        return ""
    reader = _get_geoip()
    if reader is None:
        return ""
    try:
        import geoip2.errors  # noqa: F401

        try:
            resp = reader.country(ip)
            code = getattr(resp, "country", None)
            iso = getattr(code, "iso_code", "") if code else ""
            if iso:
                return _REGION_TO_COUNTRY.get(iso.upper(), iso.upper())
        except Exception:  # noqa: BLE001
            pass
        try:
            resp = reader.city(ip)
            c = getattr(resp, "country", None)
            iso = getattr(c, "iso_code", "") if c else ""
            if iso:
                return _REGION_TO_COUNTRY.get(iso.upper(), iso.upper())
        except Exception:  # noqa: BLE001
            pass
    except Exception as exc:  # noqa: BLE001
        logger.debug("GeoIP lookup fail %s: %s", ip, exc)
    return ""


def resolve_country(request) -> str:
    """Pays : GeoIP2 → Accept-Language → vide."""
    ip = ""
    forwarded = request.META.get("HTTP_X_FORWARDED_FOR", "")
    if forwarded:
        ip = forwarded.split(",")[0].strip()
    else:
        ip = request.META.get("REMOTE_ADDR", "")
    name = country_from_ip(ip)
    if name:
        return name
    return country_from_accept_language(request.META.get("HTTP_ACCEPT_LANGUAGE", ""))
