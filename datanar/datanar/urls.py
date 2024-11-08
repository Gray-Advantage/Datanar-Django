from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("", include("homepage.urls")),
    path("admin/", admin.site.urls),
    path("api/v1/", include("api.urls")),
    path("auth/", include("users.urls")),
    path("auth/", include("allauth.urls")),
    path("dashboard/", include("dashboard.urls")),
    path("i18n/", include("django.conf.urls.i18n")),
    path("qr_code/", include("qr_codes.urls")),
    path("statistics/", include("statistic.urls")),
    path("tz_detect/", include("tz_detect.urls")),
    path("", include("redirects.urls")),
]

if settings.DEBUG and settings.NOT_TESTING:
    import debug_toolbar

    urlpatterns.append(path("__debug__/", include(debug_toolbar.urls)))
    urlpatterns.append(
        *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
    )


__all__ = []
