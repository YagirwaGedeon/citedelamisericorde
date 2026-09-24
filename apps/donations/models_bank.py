"""Confirmations de virement bancaire (dons nationaux & internationaux)."""

from pathlib import Path

from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.core.validators import FileExtensionValidator, MinValueValidator
from django.db import models

from apps.core.models import TimeStampedModel
from apps.donations.models import Donation

# Stockage hors MEDIA_ROOT : la preuve n'est jamais servie publiquement.
BANK_PROOF_STORAGE = FileSystemStorage(
    location=str(Path(settings.BASE_DIR) / "private" / "bank_transfers"),
)


class BankTransferConfirmation(TimeStampedModel):
    """Demande de confirmation envoyée par le donateur après un virement."""

    STATUSES = [
        ("pending", "En attente"),
        ("verified", "Vérifié"),
        ("rejected", "Rejeté"),
    ]

    CURRENCIES = [
        ("USD", "USD ($)"),
        ("EUR", "EUR (€)"),
        ("CDF", "CDF (FC)"),
        ("GBP", "GBP (£)"),
        ("CAD", "CAD ($)"),
        ("CHF", "CHF"),
        ("Other", "Autre"),
    ]

    donation = models.ForeignKey(
        Donation,
        verbose_name="Don lié",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="bank_transfers",
    )
    full_name = models.CharField("Nom complet", max_length=200)
    email = models.EmailField("Adresse e-mail")
    country = models.CharField("Pays", max_length=100)
    amount = models.DecimalField(
        "Montant envoyé",
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(0.01)],
    )
    currency = models.CharField("Devise", max_length=10, choices=CURRENCIES, default="USD")
    transfer_date = models.DateField("Date du virement")
    transaction_reference = models.CharField(
        "N° / référence de transaction", max_length=120, db_index=True
    )
    proof = models.FileField(
        "Preuve de paiement",
        upload_to="%Y/%m/",
        storage=BANK_PROOF_STORAGE,
        blank=True,
        validators=[FileExtensionValidator(["pdf", "png", "jpg", "jpeg", "webp"])],
        help_text="Reçu bancaire, capture d’écran ou PDF (5 Mo max).",
    )
    status = models.CharField(
        "Statut", max_length=12, choices=STATUSES, default="pending", db_index=True
    )
    admin_note = models.TextField("Note interne (admin)", blank=True)
    reviewed_at = models.DateTimeField("Vérifié le", null=True, blank=True)

    class Meta:
        verbose_name = "confirmation de virement"
        verbose_name_plural = "Virements bancaires"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["status", "created_at"]),
            models.Index(fields=["country"]),
            models.Index(fields=["transfer_date"]),
        ]

    def __str__(self):
        return f"{self.full_name} — {self.amount} {self.currency} ({self.status})"

    @property
    def status_badge(self) -> str:
        return {
            "pending": "badge-amber",
            "verified": "badge-green",
            "rejected": "badge-red",
        }.get(self.status, "badge-gray")
