"""Contrôle d'accès de l'espace /admin/."""

from functools import wraps

from django.contrib import messages
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.shortcuts import redirect
from django.urls import reverse

STAFF_ROLES = {"superadmin", "admin", "editor", "project_manager", "finance_manager"}


def _can_access(user) -> bool:
    if not user.is_authenticated:
        return False
    if user.is_staff or user.is_superuser:
        return True
    return getattr(user, "role", "") in STAFF_ROLES


def staff_login_required(view_func):
    """Exige un compte autorisé ; sinon redirection vers /admin/login/."""

    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        if not request.user.is_authenticated:
            login_url = reverse("adminpanel:login")
            from django.contrib.auth.views import redirect_to_login

            return redirect_to_login(
                request.get_full_path(), login_url, REDIRECT_FIELD_NAME
            )
        if not _can_access(request.user):
            messages.error(request, "Votre compte n'a pas accès à l'espace administration.")
            return redirect("adminpanel:login")
        return view_func(request, *args, **kwargs)

    return _wrapped
