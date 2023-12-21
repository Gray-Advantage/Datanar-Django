from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    avatar = models.ImageField(
        _("avatar"),
        upload_to="avatars/",
        null=True,
        blank=True,
    )

    def has_avatar(self):
        return self.avatar and self.avatar.url is not None


__all__ = [User]
