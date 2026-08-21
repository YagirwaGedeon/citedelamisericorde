"""Équipe technique et dirigeante (§2.2 — À propos : Équipe dirigeante)."""

from django.db import models


class TeamMember(models.Model):
    name = models.CharField("Nom complet", max_length=120)
    role = models.CharField("Fonction", max_length=160)
    formation = models.CharField("Formation", max_length=220, blank=True)
    bio = models.TextField("Biographie", blank=True)
    photo = models.ImageField("Photo", upload_to="team/", blank=True)
    order = models.PositiveIntegerField("Ordre d'affichage", default=0)
    is_published = models.BooleanField("Publié", default=True)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "Membre de l'équipe"
        verbose_name_plural = "Membres de l'équipe"

    def __str__(self):
        return self.name