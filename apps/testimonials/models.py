"""Témoignages authentiques (§15).

Règle : jamais de faux témoignages. Chaque témoignage exige une autorisation
de publication (notamment pour les bénéficiaires mineurs, §30).
"""

from django.conf import settings
from django.db import models

from apps.core.models import TimeStampedModel
from apps.media.models import MediaItem


class Testimonial(TimeStampedModel):
    """Témoignage d'un bénéficiaire, d'un donateur ou d'un partenaire."""

    KINDS = [
        ("beneficiary", "Bénéficiaire"),
        ("donor", "Donateur"),
        ("partner", "Partenaire"),
        ("volunteer", "Bénévole"),
    ]

    author_name = models.CharField("Nom de la personne", max_length=200, blank=True)
    kind = models.CharField("Profil", max_length=20, choices=KINDS, default="beneficiary")
    role_or_relation = models.CharField("Rôle / lien avec l'organisation", max_length=200, blank=True)
    content = models.TextField("Témoignage")
    photo = models.ForeignKey(
        MediaItem, verbose_name="Photo (optionnelle)", on_delete=models.SET_NULL, null=True, blank=True
    )
    related_project = models.ForeignKey(
        "projects.Project", verbose_name="Projet lié", on_delete=models.SET_NULL, null=True, blank=True
    )
    is_published = models.BooleanField("Publié", default=False)
    publication_authorized = models.BooleanField(
        "Autorisation de publication (écrite)",
        default=False,
        help_text="Obligatoire pour les témoignages de bénéficiaires (§30).",
    )
    sort_order = models.PositiveSmallIntegerField("Ordre d'affichage", default=0)
    validated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name="Validé par", on_delete=models.SET_NULL, null=True, blank=True
    )
    validated_at = models.DateTimeField("Validé le", null=True, blank=True)

    class Meta:
        verbose_name = "témoignage"
        verbose_name_plural = "témoignages"
        ordering = ["sort_order", "-created_at"]

    def __str__(self):
        return self.author_name or f"Témoignage #{self.pk}"
