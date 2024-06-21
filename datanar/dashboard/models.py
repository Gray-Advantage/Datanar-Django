import re

from django.db import models
from django.utils.translation import gettext_lazy as _


class BlockedDomainManager(models.Manager):
    def is_blocked(self, url):
        for domain in self.all():
            if re.search(domain.domain_regex, url):
                return True
        return False


class BlockedDomain(models.Model):
    objects = BlockedDomainManager()

    domain_regex = models.CharField(
        _("domain_regex"),
        help_text=_("domain_regex_that_will_be_prohibited_from_shortening"),
        max_length=255,
    )

    class Meta:
        verbose_name = _("domain_regex")
        verbose_name_plural = _("domains_regex")

    def __str__(self):
        return _("domain_regex").capitalize()


__all__ = [BlockedDomain]
