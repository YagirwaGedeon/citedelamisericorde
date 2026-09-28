"""Admin : messages de contact."""

from django.contrib import admin
from django.utils import timezone

from apps.core.admin_site import admin_site

from apps.contact.models import ContactMessage


@admin_site.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "subject", "is_read", "is_spam", "created_at")
    list_filter = ("subject", "is_read", "is_spam")
    search_fields = ("name", "email", "message")
    readonly_fields = ("created_at", "updated_at")
    actions = ["mark_as_read", "mark_as_unread"]

    def has_add_permission(self, request):
        return False

    def changeform_view(self, request, object_id=None, form_url="", extra_context=None):
        if object_id and request.method == "GET":
            ContactMessage.objects.filter(pk=object_id, is_read=False).update(
                is_read=True, read_at=timezone.now()
            )
        return super().changeform_view(request, object_id, form_url, extra_context)

    @admin.action(description="Marquer comme lu")
    def mark_as_read(self, request, queryset):
        updated = queryset.filter(is_read=False).update(is_read=True, read_at=timezone.now())
        self.message_user(request, f"{updated} message(s) marqué(s) comme lu(s).")

    @admin.action(description="Marquer comme non lu")
    def mark_as_unread(self, request, queryset):
        updated = queryset.filter(is_read=True).update(is_read=False, read_at=None)
        self.message_user(request, f"{updated} message(s) marqué(s) comme non lu(s).")
