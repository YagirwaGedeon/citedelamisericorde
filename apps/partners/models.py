"""Partenaires et donateurs institutionnels."""

from django.db import models

from apps.core.models import TimeStampedModel
from apps.media.models import MediaItem


class Partner(TimeStampedModel):
    """Partenaire, donateur institutionnel ou organisation."""

    KINDS = [
        ("partner", "Partenaire"),
        ("donor", "Donateur institutionnel"),
        ("institution", "Institution"),
        ("media", "Média"),
    ]

    name = models.CharField("Nom", max_length=200)
    kind = models.CharField("Type", max_length=20, choices=KINDS, default="partner")
    logo = models.ForeignKey(
        MediaItem, verbose_name="Logo", on_delete=models.SET_NULL, null=True, blank=True
    )
    website = models.URLField("Site web", blank=True)
    description = models.TextField("Description", blank=True)
    is_published = models.BooleanField("Publié", default=False)
    sort_order = models.PositiveSmallIntegerField("Ordre d'affichage", default=0)

    class Meta:
        verbose_name = "partenaire"
        verbose_name_plural = "partenaires"
        ordering = ["sort_order", "name"]

    def __str__(self):
        return self.name
