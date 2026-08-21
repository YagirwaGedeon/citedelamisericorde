"""Newsletter : inscription, confirmation, désinscription, export CSV."""

import secrets

from django.db import models

from apps.core.models import TimeStampedModel


class Subscriber(TimeStampedModel):
    """Abonné à la newsletter."""

    email = models.EmailField("Email", unique=True)
    name = models.CharField("Nom", max_length=200, blank=True)
    token = models.CharField(
        "Jeton de désinscription", max_length=64, unique=True, default=secrets.token_urlsafe, editable=False
    )
    is_confirmed = models.BooleanField("Confirmé", default=False)
    confirmed_at = models.DateTimeField("Confirmé le", null=True, blank=True)
    is_active = models.BooleanField("Actif", default=True)
    unsubscribed_at = models.DateTimeField("Désinscrit le", null=True, blank=True)
    source = models.CharField("Origine de l'inscription", max_length=100, blank=True)

    class Meta:
        verbose_name = "abonné"
        verbose_name_plural = "abonnés"
        ordering = ["-created_at"]
        indexes = [models.Index(fields=["is_active"])]

    def __str__(self):
        return self.email

    @property
    def is_subscribed(self) -> bool:
        return self.is_active and self.is_confirmed
