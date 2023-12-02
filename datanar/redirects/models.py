from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone


class RedirectManager(models.Manager):
    def get_by_short_link(self, short_url):
        redirect = self.get_queryset.filter(short_url=short_url).first()
        all_good = True

        if redirect is None:
            return None
        if redirect.created_at + redirect.validity_days < timezone.now():
            all_good = False
        if redirect.validity_clicks == 0:
            all_good = False

        if all_good:
            return redirect
        else:
            redirect.delete()
            redirect.save()

        return None


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
    )
    validity_days = models.PositiveIntegerField(
        _("valid_day_number"),
        help_text=_("how_many_day_link_will_be_valid"),
        default=90,
        null=True,
    )
    validity_clicks = models.PositiveIntegerField(
        _("valid_click_number"),
        help_text=_("how_many_click_on_link_will_be_valid"),
        default=None,
        null=True,
    )

    class Meta:
        verbose_name = _("redirect")
        verbose_name_plural = _("redirects")

    def __str__(self):
        return str(_("redirect")).capitalize()


__all__ = [Redirect]
