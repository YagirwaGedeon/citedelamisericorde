"""Analytics : vues de pages légères (les agrégats GA4/Matomo restent externes)."""

from django.db import models

from apps.core.models import TimeStampedModel


class PageView(TimeStampedModel):
    """Enregistrement minimal d'une visite de page (privacy-friendly)."""

    path = models.CharField("Chemin", max_length=500, db_index=True)
    country = models.CharField(
        "Pays", max_length=100, blank=True, db_index=True,
        help_text="Via GeoIP2 si configuré, sinon Accept-Language.",
    )
    referrer = models.CharField("Origine (referrer)", max_length=500, blank=True)
    is_bot = models.BooleanField("Robot détecté", default=False)
    visitor_key = models.CharField(
        "Visiteur (hash)", max_length=64, blank=True, db_index=True,
        help_text="Hash IP+UA pour visiteurs uniques (pas d’IP en clair).",
    )

    class Meta:
        verbose_name = "vue de page"
        verbose_name_plural = "vues de pages"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["created_at"]),
            models.Index(fields=["path", "created_at"]),
            models.Index(fields=["country", "created_at"]),
            models.Index(fields=["visitor_key", "created_at"]),
        ]

    def __str__(self):
        return f"{self.path} ({self.created_at:%Y-%m-%d %H:%M})"


class DailyStats(TimeStampedModel):
    """Agrégat journalier pour le dashboard (visiteurs, pages vues)."""

    date = models.DateField("Date", unique=True)
    visits = models.PositiveIntegerField("Visites", default=0)
    unique_visitors = models.PositiveIntegerField("Visiteurs uniques", default=0)
    top_pages = models.JSONField("Pages les plus vues", default=dict, blank=True)

    class Meta:
        verbose_name = "statistique quotidienne"
        verbose_name_plural = "statistiques quotidiennes"
        ordering = ["-date"]

    def __str__(self):
        return f"{self.date}: {self.visits} visites"
