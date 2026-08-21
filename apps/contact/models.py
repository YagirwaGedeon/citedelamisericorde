"""Messages de contact (§32)."""

from django.db import models

from apps.core.models import TimeStampedModel


class ContactMessage(TimeStampedModel):
    """Message reçu via le formulaire de contact (anti-spam : reCAPTCHA + honeypot)."""

    SUBJECTS = [
        ("general", "Question générale"),
        ("donation", "Faire un don"),
        ("partnership", "Partenariat"),
        ("volunteering", "Bénévolat"),
        ("press", "Presse"),
    ]

    name = models.CharField("Nom", max_length=200)
    email = models.EmailField("Email")
    phone = models.CharField("Téléphone", max_length=50, blank=True)
    subject = models.CharField("Sujet", max_length=30, choices=SUBJECTS, default="general")
    message = models.TextField("Message")
    is_read = models.BooleanField("Lu", default=False)
    read_at = models.DateTimeField("Lu le", null=True, blank=True)
    is_spam = models.BooleanField("Spam", default=False, db_index=True)
    ip_address = models.GenericIPAddressField("Adresse IP", null=True, blank=True)
    user_agent = models.CharField("Navigateur", max_length=300, blank=True)

    class Meta:
        verbose_name = "message de contact"
        verbose_name_plural = "messages de contact"
        ordering = ["-created_at"]
        indexes = [models.Index(fields=["is_read"]), models.Index(fields=["is_spam"])]

    def __str__(self):
        return f"{self.name} — {self.subject}"
