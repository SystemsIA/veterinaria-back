from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ClasesConfig(AppConfig):
    name = "veterinaria_back.clases"
    verbose_name = _("Clases")

    def ready(self):
        try:
            import veterinaria_back.clases.signals  # noqa F401
        except ImportError:
            pass
