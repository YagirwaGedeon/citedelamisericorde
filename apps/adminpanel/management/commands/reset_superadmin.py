"""Diagnostic + reset du Super Admin en une commande.

Usage :
    python manage.py reset_superadmin
"""

import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Liste les users staff et force le compte Manasse Kamole / Manasse2026."

    def handle(self, *args, **options):
        User = get_user_model()
        self.stdout.write("=== USERS ===")
        for u in User.objects.all().order_by("id"):
            self.stdout.write(
                f"id={u.id} username={u.username!r} active={u.is_active} "
                f"staff={u.is_staff} super={u.is_superuser} role={getattr(u, 'role', '')!r} "
                f"check_M2026={u.check_password('Manasse2026')}"
            )

        username = "Manasse Kamole"
        # Toujours le mot de passe imposé (jamais ADMIN_INITIAL_PASSWORD
        # qui peut être défini différemment sur PythonAnywhere).
        password = "Manasse2026"

        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                "email": "manasse.kamole@citedelamisericorde.org",
                "first_name": "Manasse",
                "last_name": "Kamole",
            },
        )
        user.set_password(password)
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.role = "superadmin"
        user.save()

        # Also create a no-space alias that logs into the same person if needed
        alias_name = "ManasseKamole"
        alias, _ = User.objects.get_or_create(
            username=alias_name,
            defaults={
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
            },
        )
        alias.set_password(password)
        alias.is_staff = True
        alias.is_superuser = True
        alias.is_active = True
        alias.role = "superadmin"
        alias.save()

        for u in User.objects.filter(username__in=[username, alias_name]):
            self.stdout.write(
                self.style.SUCCESS(
                    f"OK user={u.username!r} check={u.check_password(password)} "
                    f"staff={u.is_staff} active={u.is_active}"
                )
            )
        self.stdout.write(self.style.SUCCESS("RESET_SUPERADMIN_DONE"))
