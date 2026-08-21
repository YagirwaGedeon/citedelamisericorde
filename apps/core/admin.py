"""Admin : paramètres du site."""

from django.contrib import admin

from apps.core.admin_site import admin_site
from apps.core.models import SiteSettings


@admin_site.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Identité", {"fields": ("organization_name", "legal_name", "tagline")}),
        (
            "Coordonnées",
            {"fields": ("email", "phone", "address_bukavu", "address_goma", "whatsapp", "map_embed_url")},
        ),
        ("Réseaux sociaux", {"fields": ("facebook", "instagram", "pinterest", "twitter", "youtube")}),
        (
            "Dons et PWA",
            {"fields": ("donation_currency", "pwa_theme_color")},
        ),
        (
            "Analytics et protection",
            {"fields": ("google_analytics_id", "matomo_url", "matomo_site_id", "recaptcha_site_key", "maintenance_mode")},
        ),
    )

    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False
