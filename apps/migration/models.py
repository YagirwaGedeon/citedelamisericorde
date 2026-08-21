"""Migration WordPress : traçabilité et mapping des URLs (§7, §28).

Outils : ``manage.py wordpress_audit`` / ``wordpress_import`` / ``wordpress_report``
(voir management/commands/).
Les identifiants WordPress ne sont jamais stockés ici — uniquement dans l'environnement.
"""

from django.db import models

from apps.core.models import TimeStampedModel


class URLMapping(models.Model):
    """Correspondance ancienne URL WordPress → nouvelle URL Django (§28)."""

    old_url = models.URLField("Ancienne URL (WordPress)", max_length=500, unique=True)
    new_url = models.CharField("Nouvelle URL (Django)", max_length=500, blank=True)
    mapped_at = models.DateTimeField("Mappé le", auto_now=True)

    class Meta:
        verbose_name = "correspondance d'URL"
        verbose_name_plural = "correspondances d'URL"

    def __str__(self):
        return f"{self.old_url} → {self.new_url or '(non mappé)'}"


class MigrationRun(TimeStampedModel):
    """Exécution d'une migration (audit, import)."""

    KINDS = [("audit", "Audit"), ("import", "Import"), ("report", "Rapport")]

    kind = models.CharField("Type", max_length=20, choices=KINDS, default="import")
    started_at = models.DateTimeField("Démarré le", auto_now_add=True)
    finished_at = models.DateTimeField("Terminé le", null=True, blank=True)
    status = models.CharField(
        "Statut", max_length=20,
        choices=[("RUNNING", "En cours"), ("SUCCESS", "Réussi"), ("FAILED", "Échoué")],
        default="RUNNING",
    )
    log = models.TextField("Journal", blank=True)

    class Meta:
        verbose_name = "exécution de migration"
        verbose_name_plural = "exécutions de migration"
        ordering = ["-started_at"]

    def __str__(self):
        return f"{self.kind} — {self.status} ({self.started_at:%Y-%m-%d %H:%M})"


class ImportedRecord(TimeStampedModel):
    """Trace d'un objet importé depuis WordPress (audit de fin de migration)."""

    SOURCES = [("post", "Article"), ("page", "Page"), ("media", "Média"), ("category", "Catégorie"), ("tag", "Étiquette")]

    run = models.ForeignKey(MigrationRun, verbose_name="Exécution", on_delete=models.CASCADE, related_name="records")
    source_type = models.CharField("Type source", max_length=20, choices=SOURCES)
    source_id = models.CharField("ID source", max_length=40)
    source_title = models.CharField("Titre source", max_length=300, blank=True)
    source_url = models.URLField("URL source", max_length=500, blank=True)
    destination_model = models.CharField("Modèle destination", max_length=100, blank=True)
    destination_id = models.PositiveBigIntegerField("ID destination", null=True, blank=True)
    status = models.CharField(
        "Statut", max_length=20,
        choices=[("IMPORTED", "Importé"), ("SKIPPED", "Ignoré"), ("ERROR", "Erreur")],
        default="IMPORTED",
    )
    notes = models.TextField("Notes", blank=True)

    class Meta:
        verbose_name = "élément importé"
        verbose_name_plural = "éléments importés"
        unique_together = [("run", "source_type", "source_id")]

    def __str__(self):
        return f"{self.source_type} {self.source_id} — {self.status}"
