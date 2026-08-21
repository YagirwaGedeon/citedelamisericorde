"""Fiches projets (§9 du cahier des charges).

Un projet possède : titre, contexte, problème, objectifs, bénéficiaires,
localisation, activités, résultats, photos, statut, dates, galerie, progression.
"""

from django.db import models

from apps.core.models import SlugModel, TimeStampedModel
from apps.media.models import MediaItem
from apps.programs.models import Program


class ProjectStatus(models.Model):
    name = models.CharField("Nom", max_length=100)
    code = models.SlugField("Code", max_length=40, unique=True)
    color = models.CharField("Couleur (hex)", max_length=7, default="#f59e0b")

    class Meta:
        verbose_name = "statut de projet"
        verbose_name_plural = "statuts de projet"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Project(SlugModel, TimeStampedModel):
    """Projet humanitaire présenté sur le site."""

    title = models.CharField("Titre", max_length=300)
    program = models.ForeignKey(
        Program, verbose_name="Programme", on_delete=models.SET_NULL, null=True, blank=True,
        related_name="projects",
    )
    status = models.ForeignKey(
        ProjectStatus, verbose_name="Statut", on_delete=models.PROTECT, null=True, blank=True,
        related_name="projects",
    )
    location = models.CharField("Localisation", max_length=200, blank=True)
    context = models.TextField("Contexte", blank=True)
    problem = models.TextField("Problème", blank=True)
    objectives = models.TextField("Objectifs", blank=True)
    beneficiaries = models.TextField("Bénéficiaires", blank=True)
    activities = models.TextField("Activités", blank=True)
    results = models.TextField("Résultats", blank=True)
    progress_percent = models.PositiveSmallIntegerField("Progression (%)", default=0)
    start_date = models.DateField("Date de début", null=True, blank=True)
    end_date = models.DateField("Date de fin", null=True, blank=True)
    budget = models.DecimalField("Budget", max_digits=14, decimal_places=2, null=True, blank=True)
    currency = models.CharField("Devise", max_length=3, default="USD")
    cover_image = models.ForeignKey(
        MediaItem, verbose_name="Image de couverture", on_delete=models.SET_NULL, null=True, blank=True,
        related_name="project_cover",
    )
    gallery = models.ManyToManyField(
        MediaItem, verbose_name="Galerie", blank=True, related_name="projects"
    )
    is_featured = models.BooleanField("Projet à la une", default=False)
    publication_authorized = models.BooleanField(
        "Publication autorisée",
        default=False,
        help_text="Autorisation écrite de publication des photos/bénéficiaires (§30).",
    )
    needs_donation = models.BooleanField("Accepte les dons ciblés", default=False)
    seo_description = models.CharField("Description SEO", max_length=300, blank=True)

    class Meta:
        verbose_name = "projet"
        verbose_name_plural = "projets"
        ordering = ["-start_date", "title"]
        indexes = [models.Index(fields=["status", "start_date"])]

    def __str__(self):
        return self.title

    @property
    def is_ongoing(self) -> bool:
        return bool(self.status and self.status.code == "ongoing")
