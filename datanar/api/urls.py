from django.urls import path, re_path
from rest_framework.authtoken import views as rest_views
from rest_framework.routers import DefaultRouter

from api import views


app_name = "api"

router = DefaultRouter()
router.register("redirects", views.RedirectViewSet, basename="redirect")

urlpatterns = [
    path("docs/", views.APIDocumentationView.as_view(), name="api_docs"),
    path("api-token-auth/", rest_views.obtain_auth_token, name="get_token"),
    path(
        "api-token-auth-update/",
        views.CreateNewTokenView.as_view(),
        name="create_new_token",
    ),
    *router.urls,
    re_path(".*/", views.DefaultWrongView.as_view()),
]


__all__ = []
