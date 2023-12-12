from django.contrib.auth.models import (
    AbstractUser,
    UserManager as DjangoUserManager,
)
from django.db import models


class UserManager(DjangoUserManager):
    def get_active(self):
        return self.get_queryset().filter(is_active=True)

    def by_mail(self, email):
        return self.get_queryset().get(email=email)


class User(AbstractUser):
    objects = UserManager()
    email = models.EmailField(unique=True)


__all__ = [User]
