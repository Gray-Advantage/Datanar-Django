from django.db import models
from django.utils.translation import gettext_lazy as _

from redirects import models as redirects_models


class Click(models.Model):
    clicked_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_("redirect_time")
    )
    redirect = models.OneToOneField(
        redirects_models.Redirect, on_delete=models.CASCADE
    )
    os = models.TextField(
        verbose_name=_("os"),
        help_text=_("operating_system_from_which_redirect_was_made"),
        null=True,
    )
    browser = models.TextField(
        verbose_name=_("browser"),
        help_text=_("browser_from_which_redirect_was_made"),
        null=True,
    )
    country = models.TextField(verbose_name=_("country"), null=True)
    city = models.TextField(verbose_name=_("city"), null=True)
    referrer = models.TextField(null=True)


__all__ = [Click]
