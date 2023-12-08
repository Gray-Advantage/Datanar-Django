from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _

from core.forms import BootstrapFormMixin
from users.models import User


class UserForm(BootstrapFormMixin, UserChangeForm):
    password = None

    class Meta(UserChangeForm.Meta):
        model = get_user_model()

        fields = [
            User.username.field.name,
            User.first_name.field.name,
            User.last_name.field.name,
            User.email.field.name,
        ]
        exclude = [User.password.field.name]


class DatanarAuthenticationForm(BootstrapFormMixin, AuthenticationForm):
    pass


class DatanarUserCreationForm(BootstrapFormMixin, UserCreationForm):
    email = forms.EmailField(label=_("email"))

    class Meta(UserCreationForm.Meta):
        model = get_user_model()

        fields = [
            User.username.field.name,
            User.email.field.name,
            "password1",
            "password2",
        ]

    def clean_username(self):
        username = self.cleaned_data["username"]
        try:
            get_user_model().objects.get(username=username)
        except get_user_model().DoesNotExist:
            return username
        raise forms.ValidationError(self.error_messages["duplicate_username"])


class DatanarPasswordChangeForm(BootstrapFormMixin, PasswordChangeForm):
    pass


class DatanarPasswordResetForm(BootstrapFormMixin, PasswordResetForm):
    pass


class DatanarPasswordResetConfirmForm(BootstrapFormMixin, SetPasswordForm):
    pass


__all__ = [
    UserForm,
    DatanarAuthenticationForm,
    DatanarUserCreationForm,
    DatanarPasswordChangeForm,
    DatanarPasswordResetForm,
    DatanarPasswordResetConfirmForm,
]
