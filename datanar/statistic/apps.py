from django.apps import AppConfig
from django.utils.functional import lazy
from django.utils.translation import gettext_lazy as _


class StatisticConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "statistic"
    verbose_name = lazy(lambda: _("statistic").capitalize(), str)


__all__ = []
