from django.contrib.gis.geoip2 import GeoIP2
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _
from django.views.generic import View
from geoip2.errors import AddressNotFoundError

from redirects.forms import PasswordForm
from redirects.models import Redirect
from statistic.models import Click

geo_ip = GeoIP2()


class RedirectView(View):
    def get(self, request, *args, **kwargs):
        redirect = Redirect.objects.get_by_short_link(kwargs["short_link"])

        if redirect is None:
            raise Http404

        if redirect.password is not None:
            form = PasswordForm()
            return render(request, "redirect/redirect.html", {"form": form})

        return self.perform_redirect(redirect)

    def post(self, request, *args, **kwargs):
        redirect = Redirect.objects.get_by_short_link(kwargs["short_link"])
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
            referrer=self.request.META.get("HTTP_REFERER", None),
        )

        return HttpResponseRedirect(redirect.long_link)


__all__ = [RedirectView]
