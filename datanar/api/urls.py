from django.urls import path
from rest_framework.authtoken import views as rest_views
from rest_framework.routers import DefaultRouter

from api import views


class OptionalSlashRouter(DefaultRouter):
    def __init__(self):
        super().__init__()
        self.trailing_slash = "/?"


app_name = "api"

router = OptionalSlashRouter()
router.register("redirects", views.RedirectViewSet, basename="redirect")

urlpatterns = [
    path("docs/", views.APIDocsPreambleView.as_view(), name="docs_preamble"),
    path("api-token-auth/", rest_views.obtain_auth_token, name="get_token"),
    path(
        "api-token-auth-update/",
        views.CreateNewTokenView.as_view(),
        name="docs_create_new_token",
    ),
    path(
        "docs/qr_code_get",
        views.APIDocsQRCodeGetView.as_view(),
        name="docs_qr_code_get",
    ),
    path(
        "docs/redirect_get",
        views.APIDocsRedirectGetView.as_view(),
        name="docs_redirect_get",
    ),
    path(
        "docs/redirect_create",
        views.APIDocsRedirectCreateView.as_view(),
        name="docs_redirect_create",
    ),
    path(
        "docs/redirect_delete",
        views.APIDocsRedirectDeleteView.as_view(),
        name="docs_redirect_delete",
    ),
    path(
        "docs/token_get",
        views.APIDocsTokenGetView.as_view(),
        name="docs_token_get",
    ),
    path(
        "docs/token_create",
        views.APIDocsTokenCreateView.as_view(),
        name="docs_token_create",
    ),
    *router.urls,
]


__all__ = []
