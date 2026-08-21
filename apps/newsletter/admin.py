"""Admin : newsletter."""

from django.contrib import admin
from apps.core.admin_site import admin_site

from apps.newsletter.models import Subscriber


@admin_site.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ("email", "name", "is_confirmed", "is_active", "confirmed_at", "created_at")
    list_filter = ("is_confirmed", "is_active", "source")
    search_fields = ("email", "name")
    readonly_fields = ("token", "created_at", "updated_at")

    def has_add_permission(self, request):
        return False
