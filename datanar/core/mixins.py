from django.contrib.auth.mixins import AccessMixin
from django.http import Http404, HttpResponseRedirect
from django.views.generic import View


class RedirectToLastPageMixin:
    class SpecialEmptyPage(Exception):
        pass

    def paginate_queryset(self, queryset, page_size):
        try:
            return super().paginate_queryset(queryset, page_size)
        except Http404 as err:
            page = (
                self.kwargs.get(self.page_kwarg)
                or self.request.GET.get(self.page_kwarg)
                or "1"
            )
            if page.isdigit():
                raise self.SpecialEmptyPage
            raise err

    def get(self, request, *args, **kwargs):
        try:
            return super().get(request, *args, **kwargs)
        except self.SpecialEmptyPage:
            query_params = request.GET.copy()
            query_params.pop(self.page_kwarg, None)

            paginator = self.get_paginator(
                self.get_queryset(),
                self.get_paginate_by(self.get_queryset()),
            )
            last_page = paginator.num_pages

            return HttpResponseRedirect(
                f"{request.path}?{query_params.urlencode()}"
                f"{'&' if query_params.urlencode() else ''}"
                f"{self.page_kwarg}={last_page}",
            )


class FormMethodExtender(View):
    def post(self, request, *args, **kwargs):
        method = request.POST.get("_method", None)
        if method:
            request.method = method
            return super().dispatch(request, *args, **kwargs)
        return super().post(request, *args, **kwargs)


class StaffUserRequiredMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_staff:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


__all__ = [FormMethodExtender, StaffUserRequiredMixin]
