"""Utilisateurs et rôles.

Rôles métier (groupes Django) :
    - superadmin   : accès complet
    - admin        : gestion générale
    - editor       : articles et pages
    - project_manager : projets et programmes
    - finance_manager : donations et rapports
    - author       : articles

Le modèle User étend AbstractUser afin de conserver les permissions Django
(telles que requises par le cahier des charges §22).
"""

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Utilisateur du site. Étend le modèle Django par défaut."""

    ROLES = [
        ("superadmin", "Super Admin"),
        ("admin", "Administrateur"),
        ("editor", "Éditeur"),
        ("project_manager", "Gestionnaire de projets"),
        ("finance_manager", "Gestionnaire financier"),
        ("author", "Auteur"),
    ]

    role = models.CharField(
        "Rôle métier",
        max_length=30,
        choices=ROLES,
        default="author",
        help_text="Rôle métier ; les permissions fines passent par les groupes Django.",
    )
    phone = models.CharField("Téléphone", max_length=30, blank=True)
    photo = models.ImageField("Photo", upload_to="accounts/photos/", blank=True)
    email_verified = models.BooleanField("Email vérifié", default=False)
    is_public = models.BooleanField(
        "Visible sur le site",
        default=False,
        help_text="Uniquement si la personne a donné son accord de publication.",
    )
    bio = models.TextField("Biographie courte", blank=True)

    class Meta:
        verbose_name = "utilisateur"
        verbose_name_plural = "utilisateurs"
        ordering = ["-is_staff", "last_name", "first_name"]

    def __str__(self):
        return self.get_full_name() or self.username

    @property
    def is_team_member(self) -> bool:
        return self.is_public and self.is_active

    def assign_role_group(self) -> None:
        """Affecte l'utilisateur au groupe Django correspondant à son rôle."""
        group_name = {
            "superadmin": "Super Admin",
            "admin": "Administrateur",
            "editor": "Éditeur",
            "project_manager": "Gestionnaire de projets",
            "finance_manager": "Gestionnaire financier",
            "author": "Auteur",
        }.get(self.role)
        if group_name:
            from django.contrib.auth.models import Group

            group, _ = Group.objects.get_or_create(name=group_name)
            self.groups.add(group)
