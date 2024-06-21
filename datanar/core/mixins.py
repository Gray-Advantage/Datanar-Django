from django.contrib.auth.mixins import AccessMixin
from django.views.generic import View


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
