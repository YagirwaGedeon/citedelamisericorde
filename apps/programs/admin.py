"""Admin : programmes."""

from django.contrib import admin
from apps.core.admin_site import admin_site

from apps.programs.models import Program


@admin_site.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ("title", "domain", "is_active", "order")
    list_filter = ("is_active", "domain")
    search_fields = ("title", "description")
    prepopulated_fields = {"slug": ("title",)}
