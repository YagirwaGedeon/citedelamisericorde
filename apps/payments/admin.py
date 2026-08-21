"""Admin : paiements."""

from django.contrib import admin
from apps.core.admin_actions import export_csv_action
from apps.core.admin_site import admin_site

from apps.payments.models import PaymentProvider, PaymentTransaction, WebhookEvent


@admin_site.register(PaymentProvider)
class PaymentProviderAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "is_active", "supported_currencies", "display_order")
    list_filter = ("is_active", "code")
    readonly_fields = ("created_at", "updated_at")


@admin_site.register(PaymentTransaction)
class PaymentTransactionAdmin(admin.ModelAdmin):
    list_display = ("donation", "provider", "amount", "currency", "status", "provider_transaction_id", "created_at")
    list_filter = ("status", "provider", "currency")
    search_fields = ("donation__reference", "provider_transaction_id")
    readonly_fields = ("created_at", "updated_at")
    actions = (export_csv_action,)
    csv_export_fields = (
        "donation__reference", "provider__name", "amount", "currency", "status",
        "provider_transaction_id", "created_at",
    )
    export_csv_action.short_description = "Exporter la sélection en CSV"


@admin_site.register(WebhookEvent)
class WebhookEventAdmin(admin.ModelAdmin):
    list_display = ("provider", "event_type", "event_id", "signature_valid", "is_processed", "created_at")
    list_filter = ("provider", "signature_valid", "is_processed")
    search_fields = ("event_id", "event_type")
    readonly_fields = ("created_at", "updated_at")
