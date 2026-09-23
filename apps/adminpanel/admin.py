"""Enregistrement des modèles de l'espace admin dans l'admin Django."""

from django.contrib import admin

from apps.adminpanel.models import HomePost


@admin.register(HomePost)
class HomePostAdmin(admin.ModelAdmin):
    list_display = ("title", "status", "published_at", "order", "author")
    list_filter = ("status", "published_at")
    search_fields = ("title", "excerpt", "content")
    raw_id_fields = ("image", "author")
    date_hierarchy = "published_at"
