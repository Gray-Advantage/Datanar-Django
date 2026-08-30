from http import HTTPStatus
from io import BytesIO

from django.http import HttpResponse
from django.views import View
from PIL import Image

from qr_codes.utils import generate_qr_code


class QRCodePreview(View):
    def get(self, request, short_link):
        qr = generate_qr_code(request, short_link)

        response = HttpResponse(content_type="image/png")
        qr.save(response, kind="png", scale=10)
        return response


class QRCodeDownload(View):
    def get(self, request, img_format, short_link):
        if img_format not in ["png", "svg", "jpg", "jpeg"]:
            return HttpResponse(status=HTTPStatus.UNSUPPORTED_MEDIA_TYPE)

        qr = generate_qr_code(request, short_link)
        buffer = BytesIO()
        if img_format in ["jpg", "jpeg"]:
            qr.save(buffer, "png", scale=35)
            img = Image.open(buffer)
            content_type = "image/jpeg"
            filename_format = "jpg"
            img.convert("RGB").save(buffer, "JPEG", quality=75)
        else:
            qr.save(buffer, kind=img_format, scale=35)
            content_type = f"image/{img_format}"
            filename_format = img_format

        response = HttpResponse(buffer.getvalue(), content_type=content_type)
        response["Content-Disposition"] = (
            f'attachment; filename="qr_code.{filename_format}"'
        )
        return response


__all__ = ["QRCodeDownload", "QRCodePreview"]
