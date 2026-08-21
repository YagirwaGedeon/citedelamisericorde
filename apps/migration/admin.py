"""Admin : migration WordPress."""

from django.contrib import admin
from apps.core.admin_site import admin_site

from apps.migration.models import ImportedRecord, MigrationRun, URLMapping


@admin_site.register(URLMapping)
class URLMappingAdmin(admin.ModelAdmin):
    list_display = ("old_url", "new_url", "mapped_at")
    search_fields = ("old_url", "new_url")


@admin_site.register(MigrationRun)
class MigrationRunAdmin(admin.ModelAdmin):
    list_display = ("kind", "status", "started_at", "finished_at")
    list_filter = ("kind", "status")
    readonly_fields = ("started_at", "finished_at")

    def has_add_permission(self, request):
        return False


@admin_site.register(ImportedRecord)
class ImportedRecordAdmin(admin.ModelAdmin):
    list_display = ("source_type", "source_id", "source_title", "destination_model", "status")
    list_filter = ("source_type", "status")
    search_fields = ("source_id", "source_title")
    readonly_fields = ("created_at", "updated_at")

    def has_add_permission(self, request):
        return False
