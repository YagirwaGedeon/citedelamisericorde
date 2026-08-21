"""Médiathèque.

Chaque image est référencée une fois (déduplication par empreinte SHA-256),
avec les métadonnées exigées par le cahier des charges §29.
"""

import hashlib

from django.db import models
from django.utils import timezone

from apps.core.models import TimeStampedModel


class MediaCategory(models.Model):
    name = models.CharField("Nom", max_length=100)
    slug = models.SlugField("Slug", max_length=120, unique=True)

    class Meta:
        verbose_name = "catégorie de média"
        verbose_name_plural = "catégories de médias"
        ordering = ["name"]

    def __str__(self):
        return self.name


class MediaItem(TimeStampedModel):
    """Fichier média (image ou document)."""

    MEDIA_KINDS = [
        ("image", "Image"),
        ("document", "Document"),
    ]

    file = models.FileField("Fichier", upload_to="media/%Y/%m/")
    kind = models.CharField("Type", max_length=20, choices=MEDIA_KINDS, default="image")
    title = models.CharField("Titre", max_length=200, blank=True)
    description = models.TextField("Description", blank=True)
    alt_text = models.CharField("Texte alternatif (alt)", max_length=300, blank=True)
    category = models.ForeignKey(
        MediaCategory, verbose_name="Catégorie", on_delete=models.SET_NULL, null=True, blank=True
    )
    checksum = models.CharField("Empreinte SHA-256", max_length=64, unique=True, blank=True, db_index=True)
    width = models.PositiveIntegerField("Largeur (px)", null=True, blank=True)
    height = models.PositiveIntegerField("Hauteur (px)", null=True, blank=True)
    source_url = models.URLField("URL d'origine (WordPress)", blank=True, help_text="Laisse vide si le média est natif.")
    taken_at = models.DateTimeField("Date de prise de vue", null=True, blank=True)

    class Meta:
        verbose_name = "média"
        verbose_name_plural = "médias"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title or (self.file.name if self.file else str(self.pk))

    def save(self, *args, **kwargs):
        if not self.checksum and self.file:
            self.checksum = self._compute_checksum()
        super().save(*args, **kwargs)

    def _compute_checksum(self) -> str:
        digest = hashlib.sha256()
        try:
            self.file.seek(0)
            for chunk in self.file.chunks():
                digest.update(chunk)
            self.file.seek(0)
        except Exception:
            digest.update(str(getattr(self.file, "name", "")).encode())
        return digest.hexdigest()
