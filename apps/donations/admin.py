"""Admin : dons et donateurs."""

from django.contrib import admin
from apps.core.admin_actions import export_csv_action
from apps.core.admin_site import admin_site

from apps.donations.models import Donation, Donor


class DonationInline(admin.TabularInline):
    model = Donation
    extra = 0
    readonly_fields = ("reference", "created_at")
    can_delete = False


@admin_site.register(Donor)
class DonorAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "country", "is_anonymous", "is_recurring", "created_at")
    list_filter = ("is_anonymous", "is_recurring", "country")
    search_fields = ("name", "email", "phone")
    inlines = (DonationInline,)
    readonly_fields = ("created_at", "updated_at")


@admin_site.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = (
        "reference", "donor", "amount", "currency", "frequency", "status",
        "provider", "paid_at", "created_at",
    )
    list_filter = ("status", "frequency", "currency", "provider", "project")
    search_fields = ("reference", "donor__name", "donor__email", "provider_reference")
    readonly_fields = ("reference", "idempotency_key", "created_at", "updated_at", "receipt_pdf")
    date_hierarchy = "created_at"
    actions = (export_csv_action,)
    csv_export_fields = (
        "reference", "donor__name", "donor__email", "amount", "currency",
        "frequency", "status", "project", "provider_reference", "created_at",
    )
    export_csv_action.short_description = "Exporter la sélection en CSV"

    def has_add_permission(self, request):
        return request.user.is_superuser
