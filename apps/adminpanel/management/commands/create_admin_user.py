"""Crée (ou met à jour) le compte Super Admin de l'espace /admin/.

Usage :
    python manage.py create_admin_user
    python manage.py create_admin_user --username "Manasse Kamole" --password "…"

Le mot de passe n'est jamais stocké en clair : seul son hash (PBKDF2) est en base.
"""

import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError

DEFAULT_USERNAME = "Manasse Kamole"
DEFAULT_PASSWORD = "Manasse2026"
DEFAULT_EMAIL = "manasse.kamole@citedelamisericorde.org"


class Command(BaseCommand):
    help = "Crée ou met à jour le compte Super Admin (mot de passe hashé)."

    def add_arguments(self, parser):
        parser.add_argument("--username", default=DEFAULT_USERNAME)
        parser.add_argument("--password", default=None, help="Sinon variable ADMIN_INITIAL_PASSWORD.")
        parser.add_argument("--email", default=DEFAULT_EMAIL)
        parser.add_argument("--first-name", default="Manasse")
        parser.add_argument("--last-name", default="Kamole")

    def handle(self, *args, **options):
        User = get_user_model()
        username = options["username"]
        password = options["password"] or os.environ.get("ADMIN_INITIAL_PASSWORD") or DEFAULT_PASSWORD
        if not password or len(password) < 8:
            raise CommandError("Mot de passe trop court (8 caractères minimum).")

        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                "email": options["email"],
                "first_name": options["first_name"],
                "last_name": options["last_name"],
                "is_staff": True,
                "is_superuser": True,
                "is_active": True,
                "role": "superadmin",
            },
        )
        # Toujours hasher — jamais de mot de passe en clair en base.
        user.set_password(password)
        user.email = user.email or options["email"]
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.role = "superadmin"
        user.save()
        try:
            user.assign_role_group()
        except Exception:
            pass

        action = "créé" if created else "mis à jour"
        self.stdout.write(
            self.style.SUCCESS(
                f"Compte Super Admin « {username} » {action} "
                f"(identifiant de connexion : {username})."
            )
        )
