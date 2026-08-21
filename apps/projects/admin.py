"""Admin : projets."""

from django.contrib import admin
from apps.core.admin_site import admin_site

from apps.projects.models import Project, ProjectStatus


@admin_site.register(ProjectStatus)
class ProjectStatusAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "color")


@admin_site.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "status", "location", "progress_percent", "start_date", "is_featured", "needs_donation")
    list_filter = ("status", "program", "is_featured", "needs_donation")
    search_fields = ("title", "location", "context", "results")
    prepopulated_fields = {"slug": ("title",)}
    filter_horizontal = ("gallery",)
    readonly_fields = ("created_at", "updated_at")
    fieldsets = (
        ("Identité", {"fields": ("title", "slug", "program", "status", "location")}),
        (
            "Fiche projet (§9)",
            {"fields": ("context", "problem", "objectives", "beneficiaries", "activities", "results")},
        ),
        ("Avancement", {"fields": ("progress_percent", "start_date", "end_date", "budget", "currency")}),
        ("Médias", {"fields": ("cover_image", "gallery")}),
        ("Publication", {"fields": ("is_featured", "needs_donation", "publication_authorized", "seo_description")}),
    )
