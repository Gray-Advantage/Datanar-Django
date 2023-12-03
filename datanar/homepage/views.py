from django.contrib import messages
from django.shortcuts import render
from django.views.generic import FormView
from django.urls import reverse_lazy

from redirects.forms import RedirectForm
from redirects.models import Redirect


class HomeView(FormView):
    template_name = "homepage/main.html"
    form_class = RedirectForm
    success_url = reverse_lazy("homepage:home")

    def form_valid(self, form):
        redirect = Redirect.objects.create(**form.cleaned_data)
        redirect.save()

        messages.add_message(
            self.request,
            messages.SUCCESS,
            redirect.short_link,
        )

        return super().form_valid(form)


__all__ = [HomeView]
