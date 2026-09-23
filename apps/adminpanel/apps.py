from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AdminpanelConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.adminpanel"
    label = "adminpanel"
    verbose_name = _("Espace administration")
