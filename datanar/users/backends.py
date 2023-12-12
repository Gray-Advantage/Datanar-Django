from django.contrib.auth.backends import ModelBackend
from django.core.exceptions import ValidationError

from users.models import User


class AuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            if username is not None and "@" in username:
                user = User.objects.by_mail(username)
            elif username is None:
                user = User.objects.by_mail(kwargs["email"])
            else:
                user = User.objects.get(username=username)
        except (KeyError, ValidationError):
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return None

        if user.check_password(password) and self.user_can_authenticate(user):
            return user

        return None


__all__ = [AuthBackend]
