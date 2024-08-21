from pathlib import Path

from django.conf import settings
from django.http import HttpResponseRedirect
from django.views.generic import ListView, TemplateView

from core.mixins import (
    FormMethodExtender,
    RedirectToLastPageMixin,
    StaffUserRequiredMixin,
)
from dashboard.models import BlockedDomain
from redirects.models import Redirect


class AllLinksView(
    StaffUserRequiredMixin,
    FormMethodExtender,
    RedirectToLastPageMixin,
    ListView,
):
    template_name = "dashboard/all_links.html"
    context_object_name = "links"
    paginate_by = 6

    def get_queryset(self):
        redirects = (
            Redirect.objects.all()
            .only(Redirect.short_link.field.name)
            .order_by("-created_at")
        )
        return [redirect.short_link for redirect in redirects]

    def delete(self, request):
        Redirect.objects.filter(
            short_link=request.POST.get("short_link"),
        ).delete()
        return HttpResponseRedirect(request.get_full_path())


class BlackListView(
    StaffUserRequiredMixin,
    FormMethodExtender,
    RedirectToLastPageMixin,
    ListView,
):
    template_name = "dashboard/black_list.html"
    context_object_name = "domains"
    model = BlockedDomain
    paginate_by = 15

    def delete(self, request):
        BlockedDomain.objects.filter(id=request.POST.get("id")).delete()
        return HttpResponseRedirect(request.get_full_path())

    def patch(self, request):
        BlockedDomain.objects.filter(
            id=request.POST.get("id"),
        ).update(
            domain_regex=request.POST.get("new_domain_regex"),
        )
        return HttpResponseRedirect(request.get_full_path())

    def put(self, request):
        BlockedDomain.objects.create(
            domain_regex=request.POST.get("new_domain_regex"),
        )
        return HttpResponseRedirect(request.get_full_path())


class LogView(StaffUserRequiredMixin, FormMethodExtender, TemplateView):
    template_name = "dashboard/log.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if settings.LOG_FILE_PATH:
            with Path(settings.LOG_FILE_PATH).open("rt") as log:
                context["log"] = log.read()
        return context

    def delete(self, request):
        if settings.LOG_FILE_PATH:
            with Path(settings.LOG_FILE_PATH).open("w") as log:
                log.write("")
        return HttpResponseRedirect(request.get_full_path())


__all__ = [AllLinksView, BlackListView, LogView]
