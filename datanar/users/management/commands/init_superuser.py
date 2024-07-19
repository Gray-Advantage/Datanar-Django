from allauth.account.models import EmailAddress
from decouple import config
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Create a superuser"

    def handle(self, *args, **options):
        superuser_name = config("DATANAR_SUPERUSER_NAME", cast=str)
        superuser_email = config("DATANAR_SUPERUSER_EMAIL", cast=str)
        superuser_password = config("DATANAR_SUPERUSER_PASSWORD", cast=str)

        if not get_user_model().objects.filter(email=superuser_email).exists():
            superuser = get_user_model().objects.create_superuser(
                username=superuser_name,
                email=superuser_email,
                password=superuser_password,
            )
            EmailAddress.objects.create(
                user=superuser,
                email=superuser_email,
                primary=True,
                verified=True,
            )


__all__ = []
