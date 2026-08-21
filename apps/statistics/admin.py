"""Admin : indicateurs d'impact."""

from django.contrib import admin
from apps.core.admin_site import admin_site

from apps.statistics.models import Statistic


@admin_site.register(Statistic)
class StatisticAdmin(admin.ModelAdmin):
    list_display = ("label", "value", "prefix", "suffix", "is_published", "sort_order", "source")
    list_filter = ("is_published",)
    search_fields = ("label", "source")
    readonly_fields = ("created_at", "updated_at")

    def save_model(self, request, obj, form, change):
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)
