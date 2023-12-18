from django.contrib.auth.models import (
    AbstractUser,
    UserManager as DjangoUserManager,
)
from django.db import models
from django.utils.translation import gettext_lazy as _


class UserManager(DjangoUserManager):
    def get_active(self):
        return self.get_queryset().filter(is_active=True)

    def by_mail(self, email):
        return self.get_queryset().get(email=email)


class User(AbstractUser):
    objects = UserManager()

    avatar = models.ImageField(
        _("avatar"),
        upload_to="avatars/",
        null=True,
        blank=True,
    )

    def has_avatar(self):
        return self.avatar and self.avatar.url is not None


__all__ = [User]
