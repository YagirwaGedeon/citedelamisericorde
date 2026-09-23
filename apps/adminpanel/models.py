"""Publication d'accueil gérée depuis l'espace admin."""

from django.conf import settings
from django.db import models
from django.utils import timezone

from apps.core.models import SlugModel, TimeStampedModel
from apps.media.models import MediaItem


class HomePost(SlugModel, TimeStampedModel):
    """Carte publication affichée sur la page d'accueil."""

    STATUS = [
        ("draft", "Brouillon"),
        ("published", "Publié"),
    ]

    title = models.CharField("Titre", max_length=300)
    excerpt = models.CharField("Extrait", max_length=400, blank=True)
    content = models.TextField("Contenu (texte)", blank=True)
    image = models.ForeignKey(
        MediaItem,
        verbose_name="Image",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="home_posts",
    )
    button_text = models.CharField("Texte du bouton", max_length=80, blank=True)
    button_url = models.CharField(
        "Lien du bouton",
        max_length=300,
        blank=True,
        help_text="URL interne (ex. /projets/) ou externe (https://…).",
    )
    status = models.CharField("Statut", max_length=20, choices=STATUS, default="draft", db_index=True)
    published_at = models.DateTimeField("Date de publication", default=timezone.now, db_index=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="Auteur",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="home_posts",
    )
    order = models.PositiveSmallIntegerField("Ordre d'affichage", default=0)

    class Meta:
        verbose_name = "publication d'accueil"
        verbose_name_plural = "publications d'accueil"
        ordering = ["order", "-published_at"]
        indexes = [models.Index(fields=["status", "published_at"])]

    def __str__(self):
        return self.title

    @property
    def is_published(self) -> bool:
        return self.status == "published" and self.published_at <= timezone.now()
