from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UsersConfig(AppConfig):
    name = "fcd_community.users"
    verbose_name = _("Users")

    def ready(self):
        try:
            import fcd_community.users.signals  # noqa: F401
        except ImportError:
            pass
