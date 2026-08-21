"""Articles / Actualités.

Modèle Article avec catégories, tags, SEO, temps de lecture et le champ
``publication_authorized`` exigé par le cahier des charges §30.
"""

from django.conf import settings
from django.db import models
from django.utils import timezone

from apps.core.models import SlugModel, TimeStampedModel
from apps.media.models import MediaItem


class ArticleCategory(SlugModel):
    name = models.CharField("Nom", max_length=120)

    class Meta:
        verbose_name = "catégorie d'article"
        verbose_name_plural = "catégories d'articles"
        ordering = ["name"]

    def __str__(self):
        return self.name


class ArticleTag(SlugModel):
    name = models.CharField("Nom", max_length=80)

    class Meta:
        verbose_name = "étiquette"
        verbose_name_plural = "étiquettes"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Article(SlugModel, TimeStampedModel):
    """Article publié sur le site (actualités, événements, rapports…)."""

    STATUS = [
        ("draft", "Brouillon"),
        ("published", "Publié"),
        ("archived", "Archivé"),
    ]

    title = models.CharField("Titre", max_length=300)
    excerpt = models.TextField("Extrait", blank=True)
    content = models.TextField("Contenu (HTML purifié)", blank=True, help_text="Le HTML est nettoyé à l'enregistrement.")
    cover_image = models.ForeignKey(
        MediaItem, verbose_name="Image à la une", on_delete=models.SET_NULL, null=True, blank=True,
        related_name="article_cover",
    )
    categories = models.ManyToManyField(ArticleCategory, verbose_name="Catégories", blank=True)
    tags = models.ManyToManyField(ArticleTag, verbose_name="Étiquettes", blank=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name="Auteur", on_delete=models.SET_NULL, null=True, blank=True
    )
    status = models.CharField("Statut", max_length=20, choices=STATUS, default="draft", db_index=True)
    published_at = models.DateTimeField("Date de publication", default=timezone.now, db_index=True)
    is_featured = models.BooleanField("À la une", default=False)
    allow_comments = models.BooleanField("Commentaires autorisés", default=False)
    publication_authorized = models.BooleanField(
        "Publication autorisée",
        default=False,
        help_text="Autorisation écrite de publication des photos/enfants (§30).",
    )
    related_images = models.ManyToManyField(MediaItem, verbose_name="Galerie d'images", blank=True, related_name="articles")
    meta_title = models.CharField("Meta title (SEO)", max_length=160, blank=True)
    meta_description = models.CharField("Meta description (SEO)", max_length=300, blank=True)
    canonical_url = models.URLField("URL canonique", blank=True)
    views = models.PositiveBigIntegerField("Vues", default=0, editable=False)
    reading_time_minutes = models.PositiveSmallIntegerField("Temps de lecture (min)", default=0, editable=False)

    class Meta:
        verbose_name = "article"
        verbose_name_plural = "articles"
        ordering = ["-published_at"]
        indexes = [
            models.Index(fields=["status", "published_at"]),
            models.Index(fields=["slug"]),
        ]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.reading_time_minutes:
            words = len(self.content.replace("<", " <").split())
            self.reading_time_minutes = max(1, round(words / 200))
        super().save(*args, **kwargs)

    @property
    def is_published(self) -> bool:
        return self.status == "published" and self.published_at <= timezone.now()
