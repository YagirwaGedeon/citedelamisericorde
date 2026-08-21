"""Indicateurs d'impact (§13).

Les chiffres affichés proviennent exclusivement de la base de données et sont
modifiables depuis l'administration. Chaque indicateur référence sa source
(Audit WordPress, validation terrain…) : aucun chiffre inventé.
"""

from django.conf import settings
from django.db import models

from apps.core.models import TimeStampedModel


class Statistic(TimeStampedModel):
    """Indicateur chiffré (ex. : 200 enfants accompagnés)."""

    label = models.CharField("Libellé", max_length=200, help_text="Ex. : Enfants accompagnés")
    value = models.PositiveBigIntegerField("Valeur")
    prefix = models.CharField("Préfixe (ex. +)", max_length=10, blank=True, default="+")
    suffix = models.CharField("Suffixe (ex. %)", max_length=10, blank=True)
    icon = models.CharField("Icône (classe CSS)", max_length=80, blank=True)
    sort_order = models.PositiveSmallIntegerField("Ordre d'affichage", default=0)
    is_published = models.BooleanField("Publié", default=True)
    source = models.CharField(
        "Source du chiffre",
        max_length=300,
        blank=True,
        help_text="Référence obligatoire : rapport, audit, validation humaine…",
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name="Modifié par", on_delete=models.SET_NULL, null=True, blank=True
    )

    class Meta:
        verbose_name = "indicateur d'impact"
        verbose_name_plural = "indicateurs d'impact"
        ordering = ["sort_order"]

    def __str__(self):
        return f"{self.prefix}{self.value}{self.suffix} {self.label}"
