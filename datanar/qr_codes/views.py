from http import HTTPStatus
from io import BytesIO

from django.http import HttpResponse
from django.views import View
from PIL import Image
import segno


class QRCodePreview(View):
    def get(self, request, short_link):
        qr = segno.make_qr(
            request.build_absolute_uri(
                short_link if "/" in short_link else f"/{short_link}",
            ),
        )
        response = HttpResponse(content_type="image/png")
        qr.save(response, kind="png", scale=10)
        return response


class QRCodeDownload(View):
    def get(self, request, img_format, short_link):
        qr = segno.make_qr(
            request.build_absolute_uri(
                short_link if "/" in short_link else f"/{short_link}",
            ),
        )
        if img_format == "jpg":
            buffer = BytesIO()
            qr.save(buffer, kind="png", scale=35)
            img = Image.open(buffer)
            buffer = BytesIO()
            img.convert("RGB").save(buffer, "JPEG", quality=50)
        elif img_format in ["png", "svg"]:
            buffer = BytesIO()
            qr.save(buffer, kind=img_format, scale=35)
        else:
            return HttpResponse(
                status=HTTPStatus.UNSUPPORTED_MEDIA_TYPE,
            )

        response = HttpResponse(
            buffer.getvalue(),
            content_type=f"image/{img_format}",
        )
        response[
            "Content-Disposition"
        ] = f'attachment; filename="qr_code.{img_format}"'
        return response


__all__ = [QRCodePreview, QRCodeDownload]
