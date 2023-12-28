from django.urls import path
from rest_framework.authtoken import views as rest_views
from rest_framework.routers import DefaultRouter

from api import views


app_name = "api"


urlpatterns = [
    path("docs/", views.APIDocumentationView.as_view(), name="api_docs"),
    path("api-token-auth/", rest_views.obtain_auth_token, name="get_token"),
    path(
        "api-token-auth-update/",
        views.CreateNewTokenView.as_view(),
        name="create_new_token",
    ),
]

router = DefaultRouter()
router.register("redirects", views.RedirectViewSet, basename="redirect")
urlpatterns += router.urls


__all__ = [urlpatterns]
