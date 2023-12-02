from django.contrib.auth.models import AbstractUser
from django.db import models


class UserManager(models.Manager):
    def get_active(self):
        return self.get_queryset().filter(is_active=True)


class User(AbstractUser):
    objects = UserManager()
    email = models.EmailField(unique=True)


__all__ = [User]
