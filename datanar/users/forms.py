__all__ = (
    "DatanarChangePasswordForm",
    "DatanarEmailForm",
    "DatanarLoginForm",
    "DatanarResetPasswordForm",
    "DatanarResetPasswordKeyForm",
    "DatanarSignupForm",
    "UserForm",
)

from typing import Any

from allauth.account.forms import (
    AddEmailForm,
    ChangePasswordForm,
    LoginForm,
    ResetPasswordForm,
    ResetPasswordKeyForm,
    SignupForm,
)
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm

from core.forms import BootstrapFormMixin
from users.models import User


class UserForm(BootstrapFormMixin, UserChangeForm):
    password = None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.fields[User.email.field.name].disabled = True
        self.fields[User.avatar.field.name].widget.attrs["class"] += " d-none"

    def clean_email(self) -> str:
        return self.instance.email

    class Meta(UserChangeForm.Meta):
        model = get_user_model()

        fields = [
            User.username.field.name,
            User.email.field.name,
            User.avatar.field.name,
        ]


class DatanarEmailForm(BootstrapFormMixin, AddEmailForm):
    pass


class DatanarLoginForm(BootstrapFormMixin, LoginForm):
    pass


class DatanarSignupForm(BootstrapFormMixin, SignupForm):
    pass


class DatanarChangePasswordForm(BootstrapFormMixin, ChangePasswordForm):
    pass


class DatanarResetPasswordForm(BootstrapFormMixin, ResetPasswordForm):
    pass


class DatanarResetPasswordKeyForm(BootstrapFormMixin, ResetPasswordKeyForm):
    pass
