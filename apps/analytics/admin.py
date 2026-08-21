"""Admin : analytics."""

from django.contrib import admin
from apps.core.admin_site import admin_site

from apps.analytics.models import DailyStats, PageView


@admin_site.register(PageView)
class PageViewAdmin(admin.ModelAdmin):
    list_display = ("path", "country", "is_bot", "created_at")
    list_filter = ("is_bot", "country")
    search_fields = ("path", "referrer")
    readonly_fields = ("created_at", "updated_at")

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser


@admin_site.register(DailyStats)
class DailyStatsAdmin(admin.ModelAdmin):
    list_display = ("date", "visits", "unique_visitors")
    readonly_fields = ("date", "visits", "unique_visitors", "top_pages")

    def has_add_permission(self, request):
        return False
