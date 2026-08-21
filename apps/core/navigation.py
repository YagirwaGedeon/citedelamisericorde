"""Navigation principale (menu du site, §45)."""

from django.urls import reverse
from django.utils.translation import gettext_lazy as _


def build_menu():
    """Construit le menu principal avec URLs résolues (fallback '#' si route absente)."""
    items = [
        {"label": _("Accueil"), "name": "home"},
        {
            "label": _("À propos"),
            "name": "pages:about",
            "children": [
                {"label": _("À propos de nous"), "name": "pages:about"},
                {"label": _("Notre histoire"), "name": "pages:history"},
                {"label": _("Notre mission"), "name": "pages:mission"},
                {"label": _("Notre vision"), "name": "pages:vision"},
                {"label": _("Nos valeurs"), "name": "pages:values"},
                {"label": _("Notre équipe"), "name": "pages:team"},
            ],
        },
        {
            "label": _("Nos actions"),
            "name": "programs:list",
            "children": [
                {"label": _("Nos programmes"), "name": "programs:list"},
                {"label": _("Nos projets"), "name": "projects:list"},
                {"label": _("Notre impact"), "name": "statistics:list"},
                {"label": _("Galerie"), "name": "gallery:list"},
                {"label": _("Partenaires"), "name": "partners:list"},
            ],
        },
        {"label": _("Actualités"), "name": "articles:list"},
        {"label": _("Contact"), "name": "contact:create"},
    ]
    for item in items:
        item["url"] = _resolve(item["name"])
        if "children" in item:
            for child in item["children"]:
                child["url"] = _resolve(child["name"])
    return items


def _resolve(name: str) -> str:
    try:
        return reverse(name)
    except Exception:
        return "#"
