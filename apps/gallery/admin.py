"""Admin : galeries."""

from django.contrib import admin
from apps.core.admin_site import admin_site

from apps.gallery.models import Gallery, GalleryItem


class GalleryItemInline(admin.TabularInline):
    model = GalleryItem
    extra = 1
    autocomplete_fields = ("media",)


@admin_site.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    list_display = ("title", "is_published", "order", "created_at")
    list_filter = ("is_published",)
    search_fields = ("title", "description")
    prepopulated_fields = {"slug": ("title",)}
    inlines = (GalleryItemInline,)
