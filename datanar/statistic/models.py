from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class ClickManager(models.Manager):
    def count_for_short_link(self, short_link):
        return (
            self.get_queryset()
            .filter(redirect__short_link=short_link)
            .prefetch_related("redirect")
            .count()
        )

    def for_short_link_by_all_time(self, short_link):
        return (
            self.get_queryset()
            .filter(redirect__short_link=short_link)
            .prefetch_related("redirect")
            .only("browser", "city", "country", "redirect_id", "os")
        )

    def for_short_link_by_last_year(self, short_link):
        return self.for_short_link_by_all_time(short_link).filter(
            clicked_at__gte=timezone.now() - timezone.timedelta(days=365),
        )

    def for_short_link_by_last_month(self, short_link):
        return self.for_short_link_by_all_time(short_link).filter(
            clicked_at__gte=timezone.now() - timezone.timedelta(days=30),
        )

    def for_short_link_by_last_day(self, short_link):
        return self.for_short_link_by_all_time(short_link).filter(
            clicked_at__gte=timezone.now() - timezone.timedelta(days=1),
        )


class Click(models.Model):
    objects = ClickManager()

    clicked_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("redirect_time"),
    )
    redirect = models.ForeignKey(
        "redirects.Redirect",
        on_delete=models.CASCADE,
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


__all__ = [Click]
