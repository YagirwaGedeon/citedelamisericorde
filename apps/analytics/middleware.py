"""Middleware d'analytics : enregistre une PageView par requête publique."""

from __future__ import annotations

import logging
from hashlib import sha256

logger = logging.getLogger(__name__)

_SKIP_PREFIXES = (
    "/admin/",
    "/django-admin/",
    "/static/",
    "/media/",
    "/__debug__/",
)

_BOT_MARKERS = (
    "bot",
    "crawl",
    "spider",
    "slurp",
    "headless",
    "phantomjs",
    "curl/",
    "wget/",
    "python-requests",
    "httpclient",
    "okhttp",
    "preview",
    "monitor",
)


def _is_bot(user_agent: str) -> bool:
    if not user_agent:
        return True
    ua = user_agent.lower()
    return any(marker in ua for marker in _BOT_MARKERS)


def _client_ip(request) -> str:
    forwarded = request.META.get("HTTP_X_FORWARDED_FOR", "")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR", "unknown")


class AnalyticsMiddleware:
    """Enregistre les vues de pages (GET publics, non-bots)."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        try:
            if self._should_track(request, response):
                self._track(request)
        except Exception:  # noqa: BLE001 — ne jamais casser la réponse
            logger.exception("analytics track failed")
        return response

    @staticmethod
    def _should_track(request, response) -> bool:
        if request.method != "GET":
            return False
        status = getattr(response, "status_code", 200)
        if status >= 400:
            return False
        path = request.path
        if any(path.startswith(p) for p in _SKIP_PREFIXES):
            return False
        user = getattr(request, "user", None)
        if user is not None and user.is_authenticated:
            if user.is_staff or user.is_superuser:
                return False
        if getattr(response, "streaming", False):
            return False
        content_type = response.get("Content-Type", "") or ""
        if content_type and "text/html" not in content_type:
            return False
        return True

    @staticmethod
    def _track(request) -> None:
        from apps.analytics.geo import resolve_country
        from apps.analytics.models import PageView

        ua = request.META.get("HTTP_USER_AGENT", "")
        if _is_bot(ua):
            return

        ip = _client_ip(request)
        referrer = (request.META.get("HTTP_REFERER", "") or "")[:500]
        path = request.path[:500]
        country = resolve_country(request)
        visitor_key = sha256(f"{ip}|{ua}".encode("utf-8", "ignore")).hexdigest()[:32]

        PageView.objects.create(
            path=path,
            country=country,
            referrer=referrer,
            is_bot=False,
            visitor_key=visitor_key,
        )
