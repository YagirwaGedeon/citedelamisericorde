"""Admin : médiathèque."""

from django.contrib import admin
from apps.core.admin_site import admin_site

from apps.media.models import MediaCategory, MediaItem


@admin_site.register(MediaCategory)
class MediaCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}


@admin_site.register(MediaItem)
class MediaItemAdmin(admin.ModelAdmin):
    list_display = ("title", "kind", "category", "source_url", "width", "height", "created_at")
    list_filter = ("kind", "category")
    search_fields = ("title", "description", "alt_text", "source_url")
    readonly_fields = ("checksum", "created_at", "updated_at")
    fieldsets = (
        ("Fichier", {"fields": ("file", "kind", "category")}),
        ("Métadonnées", {"fields": ("title", "description", "alt_text", "taken_at")}),
        ("Origine", {"fields": ("source_url", "checksum", "width", "height")}),
        ("Horodatage", {"fields": ("created_at", "updated_at")}),
    )
