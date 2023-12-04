from django.http import Http404, HttpResponseRedirect
from django.views.generic import TemplateView

from redirects.models import Redirect


class RedirectView(TemplateView):
    template_name = "redirect/redirect.html"

    def get(self, request, *args, **kwargs):
        redirect = Redirect.objects.get_by_short_link(kwargs["short_link"])

        if redirect is None:
            raise Http404
        return HttpResponseRedirect(redirect.long_link)


__all__ = [RedirectView]
