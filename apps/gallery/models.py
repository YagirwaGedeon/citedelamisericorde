"""Galeries d'images."""

from django.db import models

from apps.core.models import SlugModel, TimeStampedModel
from apps.media.models import MediaItem


class Gallery(SlugModel, TimeStampedModel):
    """Galerie thématique (par projet, par événement…)."""

    title = models.CharField("Titre", max_length=200)
    description = models.TextField("Description", blank=True)
    cover = models.ForeignKey(
        MediaItem, verbose_name="Image de couverture", on_delete=models.SET_NULL, null=True, blank=True
    )
    is_published = models.BooleanField("Publiée", default=False)
    order = models.PositiveSmallIntegerField("Ordre", default=0)

    class Meta:
        verbose_name = "galerie"
        verbose_name_plural = "galeries"
        ordering = ["order", "title"]

    def __str__(self):
        return self.title


class GalleryItem(TimeStampedModel):
    """Image rattachée à une galerie."""

    gallery = models.ForeignKey(Gallery, verbose_name="Galerie", on_delete=models.CASCADE, related_name="items")
    media = models.ForeignKey(MediaItem, verbose_name="Image", on_delete=models.CASCADE)
    caption = models.CharField("Légende", max_length=300, blank=True)
    position = models.PositiveSmallIntegerField("Position", default=0)

    class Meta:
        verbose_name = "image de galerie"
        verbose_name_plural = "images de galerie"
        ordering = ["position"]
        unique_together = [("gallery", "media")]

    def __str__(self):
        return f"{self.gallery} — {self.media}"
