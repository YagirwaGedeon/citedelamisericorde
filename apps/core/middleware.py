"""Middlewares : rate limiting (§35)."""

import time
from collections import defaultdict

from django.conf import settings
from django.http import HttpResponse


class RateLimitMiddleware:
    """Limitation simple par IP (mémoire).

    En production, remplacer par une implémentation Redis (django-ratelimit).
    """

    def __init__(self, get_response):
        self.get_response = get_response
        self._store: dict[str, list[float]] = defaultdict(list)

    def __call__(self, request):
        if request.method in ("POST", "PUT", "PATCH", "DELETE"):
            max_requests = getattr(settings, "RATE_LIMIT_MAX_REQUESTS", 120)
            window = getattr(settings, "RATE_LIMIT_WINDOW_SECONDS", 60)
            now = time.monotonic()
            ip = self._client_ip(request)
            self._store[ip] = [t for t in self._store[ip] if now - t < window]
            if len(self._store[ip]) >= max_requests:
                return HttpResponse("Trop de requêtes. Réessayez plus tard.", status=429)
            self._store[ip].append(now)
        return self.get_response(request)

    @staticmethod
    def _client_ip(request) -> str:
        forwarded = request.META.get("HTTP_X_FORWARDED_FOR")
        if forwarded:
            return forwarded.split(",")[0].strip()
        return request.META.get("REMOTE_ADDR", "unknown")
