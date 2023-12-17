from django.urls import path

from statistic import views

app_name = "statistic"

urlpatterns = [
    path("my_links/", views.MyLinksView.as_view(), name="my_links"),
]
