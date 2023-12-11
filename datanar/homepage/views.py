from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import FormView

from redirects.forms import RedirectForm, RedirectFormExtended
from redirects.models import Redirect


class HomeView(FormView):
    template_name = "homepage/main.html"
    success_url = reverse_lazy("homepage:home")

    def get_form_class(self):
        if self.request.user.is_authenticated:
            return RedirectFormExtended
        return RedirectForm

    def form_valid(self, form):
        redirect = Redirect.objects.create(**form.cleaned_data)

        if self.request.user.is_authenticated:
            redirect.user = self.request.user

        redirect.save()

        messages.add_message(
            self.request,
            messages.SUCCESS,
            redirect.short_link,
        )

        return super().form_valid(form)


__all__ = [HomeView]
