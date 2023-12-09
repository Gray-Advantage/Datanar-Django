from django.urls import path

from qr_codes import views

app_name = "qr_code"

urlpatterns = [
    path(
        "preview/<short_link>/",
        views.QRCodePreview.as_view(),
        name="preview",
    ),
    path(
        "download/<img_format>/<short_link>/",
        views.QRCodeDownload.as_view(),
        name="download",
    ),
]
