"""Admin : messages de contact."""

from django.contrib import admin
from apps.core.admin_site import admin_site

from apps.contact.models import ContactMessage


@admin_site.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "subject", "is_read", "is_spam", "created_at")
    list_filter = ("subject", "is_read", "is_spam")
    search_fields = ("name", "email", "message")
    readonly_fields = ("created_at", "updated_at")

    def has_add_permission(self, request):
        return False
