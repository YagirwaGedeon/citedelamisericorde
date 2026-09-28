"""Context processors de l'espace /admin/."""

from django.db.models import Count

from apps.contact.models import ContactMessage


def admin_sidebar(request):
    """Compteur de messages non lus pour la sidebar (pages /admin/ uniquement)."""
    path = request.path
    if not (path == "/admin" or path.startswith("/admin/")):
        return {}
    user = getattr(request, "user", None)
    if not user or not user.is_authenticated:
        return {}
    if not (user.is_staff or user.is_superuser or getattr(user, "role", "") in {"superadmin", "admin", "editor", "project_manager", "finance_manager"}):
        return {}
    unread = ContactMessage.objects.filter(is_read=False, is_spam=False).count()
    return {"unread_messages": unread}
