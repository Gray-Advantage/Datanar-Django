import re

from django.db import models
from django.utils.translation import gettext_lazy as _
from link_shorteners import link_shorteners_list

BANNED_SHORTENERS = link_shorteners_list()


class BlockedDomainManager(models.Manager):
    def upgrade_regex(self, domain_regex):
        if domain_regex.startswith("|||"):
            domain_regex = r"http[s]?://(#\.)+" + domain_regex[3:]

        if domain_regex.startswith("||"):
            domain_regex = r"http[s]?://(#\.)?" + domain_regex[2:]

        if domain_regex.startswith("|"):
            domain_regex = r"http[s]?://" + domain_regex[1:]

        if "^" in domain_regex:
            domain_regex = domain_regex.replace("^", r"\.#")

        if "#" in domain_regex:
            domain_regex = domain_regex.replace("#", r".*")

        return domain_regex  # noqa R504

    def is_blocked(self, url):
        for domain in self.all():
            if re.fullmatch(self.upgrade_regex(domain.domain_regex), url):
                return True
            if any([x in url.lower() for x in BANNED_SHORTENERS]):
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
