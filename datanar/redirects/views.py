from django.contrib.gis.geoip2 import GeoIP2
from django.http import Http404, HttpResponseRedirect
from django.views.generic import TemplateView
from geoip2.errors import AddressNotFoundError

from redirects.models import Redirect
from statistic.models import Click

geo_ip = GeoIP2()


class RedirectView(TemplateView):
    template_name = "redirect/redirect.html"

    def get(self, request, *args, **kwargs):
        redirect = Redirect.objects.get_by_short_link(kwargs["short_link"])

        if redirect is None:
            raise Http404

        ip_address = request.META.get("REMOTE_ADDR", None)

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
            os=request.user_agent.os.family,
            browser=request.user_agent.browser.family,
            country=country,
            city=city,
            referrer=request.META.get("HTTP_REFERER", None),
        )

        return HttpResponseRedirect(redirect.long_link)


__all__ = [RedirectView]
