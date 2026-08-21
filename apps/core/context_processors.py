"""Context processors globaux."""

from apps.core.models import SiteSettings
from apps.core.navigation import build_menu


def site_settings(request):
    settings = SiteSettings.get()
    return {
        "site_settings": settings,
        "site_menu": build_menu(),
    }
