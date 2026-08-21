"""Programmes / domaines d'intervention.

Les quatre pôles du cahier des charges (§12) :
    - Enfants vulnérables
    - Autonomisation des femmes
    - Assistance humanitaire
    - Développement communautaire
"""

from django.db import models

from apps.core.models import SlugModel, TimeStampedModel
from apps.media.models import MediaItem


class Program(SlugModel, TimeStampedModel):
    """Domaine d'intervention de l'organisation."""

    DOMAINS = [
        ("children", "Enfants vulnérables"),
        ("women", "Autonomisation des femmes"),
        ("humanitarian", "Assistance humanitaire"),
        ("community", "Développement communautaire"),
    ]

    domain = models.CharField("Domaine", max_length=30, choices=DOMAINS, unique=True)
    title = models.CharField("Titre", max_length=200)
    short_description = models.CharField("Résumé (une phrase)", max_length=300, blank=True)
    description = models.TextField("Description", blank=True)
    icon = models.CharField("Icône (classe CSS)", max_length=80, blank=True)
    image = models.ForeignKey(
        MediaItem, verbose_name="Image", on_delete=models.SET_NULL, null=True, blank=True
    )
    is_active = models.BooleanField("Actif", default=True)
    order = models.PositiveSmallIntegerField("Ordre", default=0)

    class Meta:
        verbose_name = "programme"
        verbose_name_plural = "programmes"
        ordering = ["order", "title"]

    def __str__(self):
        return self.title
