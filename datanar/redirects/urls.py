from django.urls import path

from redirects import views

app_name = "redirects"

urlpatterns = [
    path("<short_link>/", views.RedirectView.as_view(), name="redirect"),
]
