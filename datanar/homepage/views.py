from urllib.parse import urlparse

from django.contrib import messages
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import FormView
from django.views.generic.base import TemplateView

from core.mixins import FormMethodExtender
from datanar.message_levels import LOADING_LINKS, SHORT_LINK
from redirects.forms import RedirectForm, RedirectFormExtended
from redirects.models import Redirect
from redirects.tasks import create_redirects


class HomeView(FormMethodExtender, FormView):
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

            task = create_redirects.delay(
                data,
                self.request.user.id,
                self.request.get_host(),
                self.request.META.get("HTTP_X_REAL_IP"),
            )

            messages.add_message(
                self.request,
                LOADING_LINKS,
                task.id,
            )

            return super().form_valid(form)

        if "links_file" in form.cleaned_data:
            del form.cleaned_data["links_file"]

        long_link = form.cleaned_data[Redirect.long_link.field.name]
        url_long_link = urlparse(long_link)

        if url_long_link.netloc != self.request.get_host():
            redirect = Redirect.objects.create(**form.cleaned_data)
            redirect.create_method = Redirect.CreateMethod.WEB
            redirect.ip_address = self.request.META.get("HTTP_X_REAL_IP")
            if self.request.user.is_authenticated:
                redirect.user = self.request.user
            redirect.save()
            short_link = redirect.short_link
        else:
            short_link = url_long_link.path

        messages.add_message(
            self.request,
            SHORT_LINK,
            short_link,
        )

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["SHORT_LINK"] = SHORT_LINK
        context["LOADING_LINKS"] = LOADING_LINKS
        return context

    def delete(self, request):
        Redirect.objects.filter(
            short_link=request.POST.get("short_link"),
        ).delete()
        return HttpResponseRedirect(request.get_full_path())


class ServiceRulesView(TemplateView):
    template_name = "homepage/service_rules.html"


class AboutView(TemplateView):
    template_name = "homepage/about.html"


__all__ = [HomeView, ServiceRulesView, AboutView]
