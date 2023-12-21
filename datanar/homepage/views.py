from django.contrib import messages
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.urls import reverse_lazy
from django.views.generic import FormView
from django.views.generic.base import TemplateView

from datanar.message_levels import LOADING_LINKS, SHORT_LINK
from redirects.forms import RedirectForm, RedirectFormExtended
from redirects.models import Redirect
from redirects.tasks import create_redirects


class HomeView(FormView):
    template_name = "homepage/main.html"
    success_url = reverse_lazy("homepage:home")

    def get_form_class(self):
        if self.request.user.is_authenticated:
            return RedirectFormExtended
        return RedirectForm

    def form_valid(self, form):
        if "links_file" in self.request.FILES:
            links_file = form.cleaned_data["links_file"]

            file_path = default_storage.save(
                "link-files/" + links_file.name,
                ContentFile(links_file.read()),
            )
            data = form.cleaned_data
            data["links_file"] = file_path

            task = create_redirects.delay(data, self.request.user.id)

            messages.add_message(
                self.request,
                LOADING_LINKS,
                task.id,
            )

            return super().form_valid(form)

        if "links_file" in form.cleaned_data:
            del form.cleaned_data["links_file"]

        redirect = Redirect.objects.create(**form.cleaned_data)
        if self.request.user.is_authenticated:
            redirect.user = self.request.user
        redirect.save()

        messages.add_message(
            self.request,
            SHORT_LINK,
            redirect.short_link,
        )

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        contex = super().get_context_data(**kwargs)
        contex["SHORT_LINK"] = SHORT_LINK
        contex["LOADING_LINKS"] = LOADING_LINKS
        return contex


class ServiceRulesView(TemplateView):
    template_name = "homepage/service_rules.html"


class AboutView(TemplateView):
    template_name = "homepage/about.html"


__all__ = [HomeView]
