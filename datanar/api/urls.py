from django.urls import path
from rest_framework.routers import DefaultRouter

from api import views


app_name = "api"


urlpatterns = [
    path("docs/", views.APIDocumentationView.as_view(), name="api_docs"),
]

router = DefaultRouter()
router.register(r"redirects", views.RedirectViewSet, basename="redirect")
urlpatterns += router.urls


__all__ = [urlpatterns]
