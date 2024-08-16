from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from statistic.models import Click


class RedirectManager(models.Manager):
    def get_by_short_link(self, short_link):
        redirect = self.get_queryset().filter(
            short_link=short_link,
        ).annotate(
            clicks_count=models.Count("click"),
        ).first()

        if redirect is None:
            return None

        all_good = True

        if (
            redirect.validity_days
            and redirect.is_active
            and redirect.created_at
            + timezone.timedelta(days=redirect.validity_days)
            < timezone.now()
        ):
            all_good = False

        if (
            not redirect.is_active
            and redirect.deactivated_at + timezone.timedelta(days=10)
            < timezone.now()
        ):
            redirect.delete()
            return None

        if redirect.validity_clicks:
            if redirect.clicks_count >= redirect.validity_clicks:
                all_good = False

        if not all_good:
            redirect.is_active = False
            redirect.deactivated_at = timezone.now()
            redirect.save()
            return None

        return redirect


class Redirect(models.Model):
    objects = RedirectManager()

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name=_("user"),
        help_text=_("user_who_create_bond"),
        null=True,
    )
    short_link = models.URLField(
        _("short_link"),
        help_text=_("shorten_link_to_redirect_to_resource"),
        max_length=50,
        unique=True,
    )
    long_link = models.URLField(
        _("long_link"),
        help_text=_("resource_to_which_short_link_lead"),
        max_length=2000,
    )
    created_at = models.DateTimeField(
        _("creation_time"),
        help_text=_("when_bond_was_create"),
        auto_now_add=True,
    )
    password = models.CharField(
        _("password"),
        help_text=_("password_that_will_requested_to_redirect"),
        max_length=128,
        null=True,
        blank=True,
    )
    validity_days = models.PositiveIntegerField(
        _("valid_day_number"),
        help_text=_("how_many_day_link_will_be_valid"),
        default=90,
        null=True,
        blank=True,
    )
    validity_clicks = models.PositiveIntegerField(
        _("valid_click_number"),
        help_text=_("how_many_click_on_link_will_be_valid"),
        default=None,
        null=True,
        blank=True,
    )
    is_active = models.BooleanField(
        _("active"),
        help_text=_("is_active"),
        default=True,
    )
    deactivated_at = models.DateTimeField(
        _("deactivation_time"),
        help_text=_("when_bond_was_deactivated"),
        default=None,
        null=True,
    )
    ip_address = models.GenericIPAddressField(
        _("ip_address"),
        help_text=_("client_ip_address_who_created_redirect"),
        default=None,
        null=True,
        blank=True,
    )

    class CreateMethod(models.TextChoices):
        API = "API", _("API")
        WEB = "WEB", _("Web")
        WEB_FILE = "WEB+FILE", _("Web_by_file")

    create_method = models.CharField(
        _("create_method"),
        help_text=_("method_which_redirect_was_created"),
        max_length=20,
        null=True,
        blank=True,
        choices=CreateMethod.choices,
        default=CreateMethod.WEB,
    )

    class Meta:
        verbose_name = _("redirect")
        verbose_name_plural = _("redirects")

    def __str__(self):
        return _("redirect").capitalize()


__all__ = [Redirect]
