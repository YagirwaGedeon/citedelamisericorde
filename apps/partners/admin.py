"""Admin : partenaires."""

from django.contrib import admin
from apps.core.admin_site import admin_site

from apps.partners.models import Partner


@admin_site.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ("name", "kind", "is_published", "website", "sort_order")
    list_filter = ("kind", "is_published")
    search_fields = ("name", "description")
