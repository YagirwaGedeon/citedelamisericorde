"""Dons et donateurs.

Référence de reçu : ``CMD-DON-<ANNÉE>-<NUMÉRO SÉQUENTIEL>` (§20).
Statuts exigés : PENDING / PROCESSING / SUCCEEDED / FAILED / REFUNDED / CANCELLED (§19).
"""

from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models, transaction
from django.utils import timezone

from apps.core.models import TimeStampedModel
from apps.payments.models import PaymentProvider
from apps.projects.models import Project


class Donor(TimeStampedModel):
    """Donateur (personne ou anonyme)."""

    name = models.CharField("Nom complet", max_length=200, blank=True)
    email = models.EmailField("Email", blank=True)
    phone = models.CharField("Téléphone", max_length=50, blank=True)
    country = models.CharField("Pays", max_length=100, blank=True)
    is_anonymous = models.BooleanField("Don anonyme", default=False)
    is_recurring = models.BooleanField("Donateur mensuel", default=False)
    notes = models.TextField("Notes internes", blank=True)

    class Meta:
        verbose_name = "donateur"
        verbose_name_plural = "donateurs"
        ordering = ["-created_at"]
        indexes = [models.Index(fields=["email"])]

    def __str__(self):
        if self.is_anonymous or not self.name:
            return f"Donateur anonyme #{self.pk}"
        return f"{self.name} ({self.email or 'sans email'})"


class Donation(TimeStampedModel):
    """Transaction de don (unique ou mensuelle)."""

    FREQUENCIES = [
        ("once", "Don unique"),
        ("monthly", "Don mensuel"),
    ]

    STATUSES = [
        ("PENDING", "En attente"),
        ("PROCESSING", "En traitement"),
        ("SUCCEEDED", "Réussi"),
        ("FAILED", "Échoué"),
        ("REFUNDED", "Remboursé"),
        ("CANCELLED", "Annulé"),
    ]

    reference = models.CharField(
        "Référence (reçu)", max_length=30, unique=True, editable=False, blank=True
    )
    donor = models.ForeignKey(Donor, verbose_name="Donateur", on_delete=models.PROTECT, related_name="donations")
    project = models.ForeignKey(
        Project, verbose_name="Projet", on_delete=models.SET_NULL, null=True, blank=True,
        related_name="donations",
    )
    amount = models.DecimalField(
        "Montant", max_digits=12, decimal_places=2, validators=[MinValueValidator(Decimal("0.01"))]
    )
    currency = models.CharField("Devise", max_length=3, default="USD")
    frequency = models.CharField("Fréquence", max_length=10, choices=FREQUENCIES, default="once")
    status = models.CharField("Statut", max_length=12, choices=STATUSES, default="PENDING", db_index=True)
    provider = models.ForeignKey(
        PaymentProvider, verbose_name="Passerelle", on_delete=models.SET_NULL, null=True, blank=True
    )
    provider_reference = models.CharField("Référence fournisseur", max_length=255, blank=True, db_index=True)
    idempotency_key = models.CharField(
        "Clé d'idempotence", max_length=100, unique=True, editable=False,
        help_text="Anti-double paiement (§19).",
    )
    is_anonymous = models.BooleanField("Don anonyme", default=False)
    donor_message = models.TextField("Message du donateur", blank=True)
    receipt_pdf = models.FileField("Reçu PDF", upload_to="receipts/%Y/%m/", blank=True)
    receipt_sent_at = models.DateTimeField("Email de remerciement envoyé le", null=True, blank=True)
    paid_at = models.DateTimeField("Payé le", null=True, blank=True)

    class Meta:
        verbose_name = "don"
        verbose_name_plural = "dons"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["status"]),
            models.Index(fields=["created_at"]),
            models.Index(fields=["currency", "amount"]),
        ]

    def __str__(self):
        return f"{self.reference or self.pk} — {self.amount} {self.currency} ({self.status})"

    def save(self, *args, **kwargs):
        with transaction.atomic():
            if not self.reference:
                self.reference = self._next_reference()
            super().save(*args, **kwargs)

    def _next_reference(self) -> str:
        year = timezone.now().year
        last = (
            Donation.objects.filter(reference__startswith=f"CMD-DON-{year}-")
            .order_by("-reference")
            .values_list("reference", flat=True)
            .first()
        )
        if last:
            number = int(last.rsplit("-", 1)[1]) + 1
        else:
            number = 1
        return f"CMD-DON-{year}-{number:06d}"
