from django.conf import settings
from django.views.generic import TemplateView, ListView
from django.http import HttpResponseRedirect

from core.mixins import FormMethodExtender, StaffUserRequiredMixin
from redirects.models import Redirect


class AllLinksView(StaffUserRequiredMixin, FormMethodExtender, ListView):
    template_name = "dashboard/all_links.html"
    context_object_name = "links"
    paginate_by = 6

    def get_queryset(self):
        redirects = Redirect.objects.all().only(
            Redirect.short_link.field.name
        ).order_by("-created_at")
        return [redirect.short_link for redirect in redirects]

    def delete(self, request):
        Redirect.objects.filter(
            short_link=request.POST.get("short_link"),
        ).delete()
        return HttpResponseRedirect(request.get_full_path())


class BlackListView(StaffUserRequiredMixin, TemplateView):
    template_name = "dashboard/black_list.html"


class LogView(StaffUserRequiredMixin, FormMethodExtender, TemplateView):
    template_name = "dashboard/log.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if settings.LOG_FILE_PATH:
            with open(settings.LOG_FILE_PATH, "rt") as log:
                context["log"] = log.read()
        return context

    def delete(self, request):
        if settings.LOG_FILE_PATH:
            with open(settings.LOG_FILE_PATH, "w") as log:
                log.write("")
        return HttpResponseRedirect(request.get_full_path())


__all__ = [AllLinksView, BlackListView, LogView]
