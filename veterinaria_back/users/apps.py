from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UsersConfig(AppConfig):
    name = "veterinaria_back.users"
    verbose_name = _("Users")

    def ready(self):
        try:
            import veterinaria_back.users.signals  # noqa F401
        except ImportError:
            pass
