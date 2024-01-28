from django.urls import path

from qr_codes import views

app_name = "qr_code"

urlpatterns = [
    path(
        "download/<img_format>/<path:short_link>/",
        views.QRCodeDownload.as_view(),
        name="download",
    ),
    path(
        "preview/<path:short_link>/",
        views.QRCodePreview.as_view(),
        name="preview",
    ),
]
