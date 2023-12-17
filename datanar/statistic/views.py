from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View

from redirects.models import Redirect


class MyLinksView(LoginRequiredMixin, View):
    template_name = "statistic/my_links.html"

    def get(self, request, *args, **kwargs):
        redirects = Redirect.objects.filter(user=request.user).only(
            "short_link",
        )
        context = {"messages": [redirect.short_link for redirect in redirects]}
        return render(request, "statistic/my_links.html", context)


__all__ = [MyLinksView]
