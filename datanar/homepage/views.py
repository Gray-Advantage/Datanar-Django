from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = "homepage/main.html"


__all__ = [HomeView]
