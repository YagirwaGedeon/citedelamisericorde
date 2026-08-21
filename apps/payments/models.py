"""Paiements : fournisseurs activables, transactions et webhooks (§18–19).

Aucune donnée bancaire n'est stockée. Les clés secrètes restent dans le
environnement (config/settings.py -> PAYMENT_PROVIDERS) et ne sont jamais
sérialisées en base.
"""

from django.db import models

from apps.core.models import TimeStampedModel


class PaymentProvider(TimeStampedModel):
    """Passerelle de paiement, activable/désactivable depuis l'administration (§18)."""

    CODES = [
        ("stripe", "Stripe"),
        ("paypal", "PayPal"),
        ("mobile_money", "Mobile Money (Flutterwave / Airtel / M-Pesa / Orange)"),
        ("other", "Autre fournisseur"),
    ]

    name = models.CharField("Nom", max_length=100)
    code = models.CharField("Code", max_length=30, choices=CODES, unique=True)
    is_active = models.BooleanField("Actif", default=False)
    supported_currencies = models.CharField("Devises supportées (séparées par des virgules)", max_length=100, default="USD")
    supported_countries = models.CharField(
        "Pays supportés (ISO, séparés par des virgules)", max_length=200, blank=True,
        help_text="Vérifier la disponibilité pour la RDC avant activation (§18).",
    )
    display_order = models.PositiveSmallIntegerField("Ordre d'affichage", default=0)
    logo = models.ImageField("Logo", upload_to="payments/logos/", blank=True)
    description = models.CharField("Description affichée au donateur", max_length=300, blank=True)

    class Meta:
        verbose_name = "passerelle de paiement"
        verbose_name_plural = "passerelles de paiement"
        ordering = ["display_order", "name"]

    def __str__(self):
        return self.name


class PaymentTransaction(TimeStampedModel):
    """Transaction envoyée à une passerelle."""

    STATUSES = [
        ("PENDING", "En attente"),
        ("PROCESSING", "En traitement"),
        ("SUCCEEDED", "Réussi"),
        ("FAILED", "Échoué"),
        ("REFUNDED", "Remboursé"),
        ("CANCELLED", "Annulé"),
    ]

    donation = models.ForeignKey(
        "donations.Donation", verbose_name="Don", on_delete=models.CASCADE, related_name="transactions"
    )
    provider = models.ForeignKey(PaymentProvider, verbose_name="Passerelle", on_delete=models.PROTECT)
    amount = models.DecimalField("Montant", max_digits=12, decimal_places=2)
    currency = models.CharField("Devise", max_length=3, default="USD")
    status = models.CharField("Statut", max_length=12, choices=STATUSES, default="PENDING", db_index=True)
    provider_transaction_id = models.CharField("ID transaction fournisseur", max_length=255, blank=True, db_index=True)
    raw_response = models.JSONField("Réponse brute (fournisseur)", default=dict, blank=True)
    error_message = models.TextField("Message d'erreur", blank=True)
    attempted_at = models.DateTimeField("Tentative le", null=True, blank=True)
    succeeded_at = models.DateTimeField("Réussi le", null=True, blank=True)

    class Meta:
        verbose_name = "transaction de paiement"
        verbose_name_plural = "transactions de paiement"
        ordering = ["-created_at"]
        indexes = [models.Index(fields=["status"]), models.Index(fields=["provider", "status"])]

    def __str__(self):
        return f"{self.provider.name} {self.amount} {self.currency} ({self.status})"


class WebhookEvent(TimeStampedModel):
    """Événement reçu d'une passerelle (vérification de signature obligatoire)."""

    provider = models.ForeignKey(PaymentProvider, verbose_name="Passerelle", on_delete=models.PROTECT)
    event_id = models.CharField("ID événement fournisseur", max_length=255, db_index=True)
    event_type = models.CharField("Type d'événement", max_length=100)
    payload = models.JSONField("Payload", default=dict)
    signature_valid = models.BooleanField("Signature vérifiée", default=False)
    is_processed = models.BooleanField("Traité", default=False)
    processed_at = models.DateTimeField("Traité le", null=True, blank=True)
    error_message = models.TextField("Erreur de traitement", blank=True)

    class Meta:
        verbose_name = "événement webhook"
        verbose_name_plural = "événements webhook"
        ordering = ["-created_at"]
        unique_together = [("provider", "event_id")]

    def __str__(self):
        return f"{self.provider.code} / {self.event_type} / {self.event_id}"
