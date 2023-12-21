from allauth.account.forms import AddEmailForm
from allauth.account.forms import ChangePasswordForm
from allauth.account.forms import LoginForm
from allauth.account.forms import ResetPasswordForm
from allauth.account.forms import ResetPasswordKeyForm
from allauth.account.forms import SignupForm
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm

from core.forms import BootstrapFormMixin
from users.models import User


class UserForm(BootstrapFormMixin, UserChangeForm):
    password = None

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields[User.email.field.name].widget.attrs["readonly"] = True
        self.fields[User.email.field.name].widget.attrs["disabled"] = True

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


__all__ = [
    UserForm,
    DatanarLoginForm,
    DatanarEmailForm,
    DatanarSignupForm,
    DatanarChangePasswordForm,
    DatanarResetPasswordForm,
    DatanarResetPasswordKeyForm,
]
