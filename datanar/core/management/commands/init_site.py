from decouple import config
from django.conf import settings
from django.contrib.sites.models import Site
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Create or update the Django Site"

    def handle(self, *args, **options):
        site_id = settings.SITE_ID
        site_domain = config(
            "DATANAR_SITE_DOMAIN",
            default="datanar.ru",
            cast=str,
        )
        site_name = settings.SITE_NAME

        _, created = Site.objects.update_or_create(
            pk=site_id,
            defaults={
                Site.domain.field.name: site_domain,
                Site.name.field.name: site_name,
            },
        )

        if created:
            self.stdout.write(self.style.SUCCESS(f"Created Site: {site_name}"))
        else:
            self.stdout.write(self.style.SUCCESS(f"Updated Site: {site_name}"))


__all__ = []
