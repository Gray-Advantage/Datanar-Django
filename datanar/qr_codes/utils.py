__all__ = ("generate_qr_code",)

from urllib.parse import urljoin

from django.http import HttpRequest
import segno

from core.context_processors import server_url


def generate_qr_code(request: HttpRequest, short_link: str) -> segno.QRCode:
    full_url = urljoin(server_url(request)["server_url"], short_link)
    return segno.make_qr(full_url)
