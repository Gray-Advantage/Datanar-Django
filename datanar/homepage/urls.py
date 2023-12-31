from django.urls import path

from homepage import views

app_name = "homepage"

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("about/", views.AboutView.as_view(), name="about"),
    path(
        "service_rules/",
        views.ServiceRulesView.as_view(),
        name="service_rules",
    ),
]
