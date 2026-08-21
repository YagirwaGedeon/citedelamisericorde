"""Admin : pages."""

from django.contrib import admin
from apps.core.admin_site import admin_site

from apps.pages.models import Page, Report


@admin_site.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ("title", "template", "status", "in_menu", "order", "updated_at")
    list_filter = ("status", "in_menu")
    search_fields = ("title", "content")
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ("created_at", "updated_at")


@admin_site.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ("title", "kind", "year", "is_published", "validated_by", "validated_at")
    list_filter = ("kind", "is_published")
    search_fields = ("title",)
    readonly_fields = ("created_at", "updated_at")

    def save_model(self, request, obj, form, change):
        if obj.is_published and not obj.validated_by:
            obj.validated_by = request.user
            obj.validated_at = __import__("django.utils.timezone", fromlist=["now"]).now()
        super().save_model(request, obj, form, change)
