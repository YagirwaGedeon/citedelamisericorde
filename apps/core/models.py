"""Modèles communs : SlugModel, TimeStampedModel et SiteSettings.

SlugModel et TimeStampedModel sont réutilisés par les autres apps.
"""

from django.db import models
from django.utils.text import slugify


class SlugModel(models.Model):
    """Ajoute un slug unique, auto-généré à la création si absent."""

    slug = models.SlugField("Slug", max_length=255, unique=True, blank=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(getattr(self, "title", str(self)))
            self.slug = base[:250] or f"{self.__class__.__name__.lower()}-{id(self)}"
        super().save(*args, **kwargs)


class TimeStampedModel(models.Model):
    """Ajoute les dates de création et de modification."""

    created_at = models.DateTimeField("Créé le", auto_now_add=True)
    updated_at = models.DateTimeField("Modifié le", auto_now=True)

    class Meta:
        abstract = True


class SiteSettings(models.Model):
    """Paramètres globaux du site (coordonnées, réseaux sociaux, PWA…)."""

    organization_name = models.CharField(
        "Nom de l'organisation", max_length=200, default="Cité de la Miséricorde"
    )
    legal_name = models.CharField(
        "Nom légal (ASBL)",
        max_length=200,
        blank=True,
        help_text="Ex. : Cité de la Miséricorde",
    )
    tagline = models.CharField("Slogan", max_length=200, default="Heureux ceux qui procurent la paix")
    email = models.EmailField("Email général", blank=True)
    phone = models.CharField("Téléphone", max_length=50, blank=True)
    address_bukavu = models.CharField("Adresse Bukavu", max_length=300, blank=True)
    address_goma = models.CharField("Adresse Goma", max_length=300, blank=True)
    facebook = models.URLField("Facebook", blank=True)
    instagram = models.URLField("Instagram", blank=True)
    pinterest = models.URLField("Pinterest", blank=True)
    twitter = models.URLField("X / Twitter", blank=True)
    youtube = models.URLField("YouTube", blank=True)
    whatsapp = models.CharField("WhatsApp", max_length=50, blank=True)
    map_embed_url = models.URLField("URL carte (Leaflet/OSM)", blank=True)
    donation_currency = models.CharField(
        "Devise par défaut des dons", max_length=3, default="USD"
    )
    pwa_theme_color = models.CharField("Couleur thème PWA", max_length=7, default="#0f766e")
    google_analytics_id = models.CharField("Google Analytics (GA4)", max_length=50, blank=True)
    matomo_url = models.URLField("Matomo URL", blank=True)
    matomo_site_id = models.CharField("Matomo Site ID", max_length=20, blank=True)
    recaptcha_site_key = models.CharField("reCAPTCHA v3 site key", max_length=100, blank=True)
    maintenance_mode = models.BooleanField("Mode maintenance", default=False)

    class Meta:
        verbose_name = "paramètres du site"
        verbose_name_plural = "paramètres du site"

    def __str__(self):
        return self.organization_name

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def get(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj
