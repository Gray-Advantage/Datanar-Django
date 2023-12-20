from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views as rest_views

from api import views


app_name = "api"


urlpatterns = [
    path("docs/", views.APIDocumentationView.as_view(), name="api_docs"),
    path('api-token-auth/', rest_views.obtain_auth_token)
]

router = DefaultRouter()
router.register(r"redirects", views.RedirectViewSet, basename="redirect")
urlpatterns += router.urls


__all__ = [urlpatterns]
