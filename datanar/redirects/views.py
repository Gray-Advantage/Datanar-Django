from http import HTTPStatus

from celery.result import AsyncResult
from django.contrib import messages
from django.contrib.gis.geoip2 import GeoIP2
from django.http import Http404, HttpResponseRedirect
from django.http import HttpResponse
from django.shortcuts import render, reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import View
from geoip2.errors import AddressNotFoundError

from datanar.message_levels import SHORT_LINK
from redirects.forms import PasswordForm
from redirects.models import Redirect
from statistic.models import Click

geo_ip = GeoIP2()


class RedirectView(View):
    def get(self, request, *args, **kwargs):
        redirect = Redirect.objects.get_by_short_link(
            kwargs[Redirect.short_link.field.name],
        )

        if redirect is None:
            raise Http404

        if redirect.password is not None:
            form = PasswordForm()
            return render(request, "redirect/redirect.html", {"form": form})

        return self.perform_redirect(redirect)

    def post(self, request, *args, **kwargs):
        redirect = Redirect.objects.get_by_short_link(
            kwargs[Redirect.short_link.field.name],
        )
        form = PasswordForm(request.POST)

        if (
            form.is_valid()
            and form.cleaned_data["password"] == redirect.password
        ):
            return self.perform_redirect(redirect)

        form.add_error("password", _("invalid_password"))
        return render(request, "redirect/redirect.html", {"form": form})

    def perform_redirect(self, redirect):
        ip_address = self.request.META.get("REMOTE_ADDR", None)

        try:
            country = geo_ip.country_name(ip_address)
        except AddressNotFoundError:
            country = None

        try:
            city = geo_ip.city(ip_address)["city"]
        except AddressNotFoundError:
            city = None

        Click.objects.create(
            redirect=redirect,
            os=self.request.user_agent.os.family,
            browser=self.request.user_agent.browser.family,
            country=country,
            city=city,
        )

        return HttpResponseRedirect(redirect.long_link)


class LinksFileStatus(View):
    def get(self, request, *args, **kwargs):
        task = AsyncResult(self.kwargs["work_id"])

        if not task.ready():
            return HttpResponse(status=HTTPStatus.ACCEPTED)

        for line in task.result:
            messages.add_message(request, SHORT_LINK, line)

        return HttpResponseRedirect(reverse("homepage:home"))


__all__ = [RedirectView]
