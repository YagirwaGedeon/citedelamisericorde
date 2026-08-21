"""Admin : équipe dirigeante."""

from django.contrib import admin

from apps.core.admin_site import admin_site
from apps.team.models import TeamMember


@admin_site.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ("name", "role", "order", "is_published")
    list_editable = ("order", "is_published")
    list_filter = ("is_published",)
    search_fields = ("name", "role")
    fieldsets = (
        (None, {"fields": ("name", "role", "formation", "bio", "photo")}),
        ("Publication", {"fields": ("order", "is_published")}),
    )