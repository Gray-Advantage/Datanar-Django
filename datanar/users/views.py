from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.views.generic import FormView
from django.views.generic.base import View

from users import forms
from users.models import User


class SignUpView(FormView):
    template_name = "users/signup.html"
    form_class = forms.DatanarUserCreationForm
    success_url = reverse_lazy("homepage:home")
    model = User

    def form_valid(self, form):
        user = User.objects.create_user(
            username=form.cleaned_data["username"],
            email=form.cleaned_data["email"],
            password=form.cleaned_data["password1"],
            is_active=settings.DEFAULT_USER_IS_ACTIVE,
        )

        activation_url = self.request.build_absolute_uri(
            reverse(
                "users:activate",
                args=[form.cleaned_data["username"]],
            ),
        )

        if user.is_active is False:
            send_mail(
                _("activation_of_the_datanar_account"),
                (
                    f'{_("activate_your_account_12_hours_following_link")}'
                    "\n\n"
                    f"{activation_url}"
                ),
                None,
                [form.cleaned_data["email"]],
            )
        return super().form_valid(form)


class ActivateView(View):
    def get(self, request, username):
        user = get_user_model().objects.get(username=username)
        if timezone.now() < user.date_joined + timezone.timedelta(hours=12):
            user.is_active = True
            user.save()
        return redirect("homepage:home")


__all__ = [SignUpView, ActivateView]
