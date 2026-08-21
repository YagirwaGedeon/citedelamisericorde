"""Pages statiques et documents de transparence."""

from django.conf import settings
from django.db import models

from apps.core.models import SlugModel, TimeStampedModel
from apps.media.models import MediaItem


class Page(SlugModel, TimeStampedModel):
    """Page éditoriale (À propos, Histoire, Mission, Valeurs, Équipe, Transparence…)."""

    title = models.CharField("Titre", max_length=200)
    content = models.TextField("Contenu (HTML purifié)", blank=True)
    cover_image = models.ForeignKey(
        MediaItem, verbose_name="Image de couverture", on_delete=models.SET_NULL, null=True, blank=True
    )
    template = models.CharField(
        "Gabarit", max_length=80, blank=True,
        help_text="Nom du gabarit Django (ex. 'about.html'), vide pour le gabarit par défaut.",
    )
    status = models.CharField(
        "Statut", max_length=20,
        choices=[("draft", "Brouillon"), ("published", "Publié")],
        default="draft",
    )
    order = models.PositiveSmallIntegerField("Ordre", default=0)
    in_menu = models.BooleanField("Visible dans le menu", default=False)
    meta_title = models.CharField("Meta title (SEO)", max_length=160, blank=True)
    meta_description = models.CharField("Meta description (SEO)", max_length=300, blank=True)

    class Meta:
        verbose_name = "page"
        verbose_name_plural = "pages"
        ordering = ["order", "title"]

    def __str__(self):
        return self.title


class Report(TimeStampedModel):
    """Document de transparence (rapport annuel, rapport de projet, financier…)."""

    KINDS = [
        ("annual", "Rapport annuel"),
        ("project", "Rapport de projet"),
        ("financial", "Rapport financier"),
        ("other", "Autre document"),
    ]

    title = models.CharField("Titre", max_length=250)
    kind = models.CharField("Type", max_length=20, choices=KINDS, default="annual")
    year = models.PositiveSmallIntegerField("Année", null=True, blank=True)
    document = models.FileField("Fichier PDF", upload_to="reports/%Y/")
    summary = models.TextField("Résumé", blank=True)
    is_published = models.BooleanField(
        "Publié",
        default=False,
        help_text="Tout document doit être validé par l'administration avant publication (§31).",
    )
    validated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name="Validé par", on_delete=models.SET_NULL, null=True, blank=True
    )
    validated_at = models.DateTimeField("Validé le", null=True, blank=True)
    published_at = models.DateTimeField("Publié le", null=True, blank=True)

    class Meta:
        verbose_name = "rapport / document"
        verbose_name_plural = "rapports / documents"
        ordering = ["-year", "title"]

    def __str__(self):
        return self.title
