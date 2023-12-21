from django.urls import path

from statistic import views

app_name = "statistic"

urlpatterns = [
    path(
        "download/<link>/<period>/",
        views.DownloadStatistic.as_view(),
        name="download",
    ),
    path("my_links/", views.MyLinksView.as_view(), name="my_links"),
    path(
        "my_links/<link>/<period>/",
        views.LinkDetailView.as_view(),
        name="link_detail",
    ),
]
