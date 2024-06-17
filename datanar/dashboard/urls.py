from django.contrib import admin
from django.urls import include, path

from dashboard import views

app_name = "dashboard"

urlpatterns = [
    path("all_links/", views.AllLinksView.as_view(), name="all_links"),
    path("black_list/", views.BlackListView.as_view(), name="black_list"),
    path("log/", views.LogView.as_view(), name="log"),
]


__all__ = []
