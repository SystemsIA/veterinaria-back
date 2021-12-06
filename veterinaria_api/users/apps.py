from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UsersConfig(AppConfig):
    name = "veterinaria_api.users"
    verbose_name = _("Usuarios")

    def ready(self):
        try:
            import veterinaria_api.users.signals  # noqa F401
        except ImportError:
            pass
