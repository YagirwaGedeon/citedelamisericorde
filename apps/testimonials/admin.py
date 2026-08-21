"""Admin : témoignages."""

from django.contrib import admin
from apps.core.admin_site import admin_site

from apps.testimonials.models import Testimonial


@admin_site.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ("author_name", "kind", "is_published", "publication_authorized", "validated_by", "validated_at")
    list_filter = ("kind", "is_published", "publication_authorized")
    search_fields = ("author_name", "content")
    readonly_fields = ("created_at", "updated_at")

    def save_model(self, request, obj, form, change):
        if obj.is_published and not obj.validated_by:
            obj.validated_by = request.user
            obj.validated_at = __import__("django.utils.timezone", fromlist=["now"]).now()
        super().save_model(request, obj, form, change)
