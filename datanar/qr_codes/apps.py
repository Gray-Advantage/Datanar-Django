from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class QrCodesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "qr_codes"
    verbose_name = _("qr-codes")


__all__ = []
