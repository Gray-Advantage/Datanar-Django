__all__ = ("AccountView", "PasswordChangeDoneView")

from typing import TYPE_CHECKING

from django.contrib.auth import views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView

from users.forms import UserForm

if TYPE_CHECKING:
    from django.db.models import QuerySet

    from users.models import User


class AccountView(LoginRequiredMixin, UpdateView):
    template_name = "users/profile.html"
    form_class = UserForm
    success_url = reverse_lazy("users:profile")

    def get_object(self, queryset: "QuerySet | None" = None) -> "User":
        return self.request.user


class PasswordChangeDoneView(views.PasswordChangeDoneView):
    pass
