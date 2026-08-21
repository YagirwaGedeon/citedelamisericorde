"""Admin : utilisateurs et rôles."""

from django.contrib import admin
from apps.core.admin_site import admin_site
from django.contrib.auth.admin import UserAdmin

from apps.accounts.models import User


@admin_site.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ("username", "get_full_name", "role", "is_public", "is_staff", "is_active")
    list_filter = ("role", "is_staff", "is_active", "is_public")
    search_fields = ("username", "first_name", "last_name", "email")
    fieldsets = UserAdmin.fieldsets + (
        ("Profil métier", {"fields": ("role", "phone", "photo", "bio", "email_verified", "is_public")}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Profil métier", {"fields": ("role", "phone", "email")}),
    )
