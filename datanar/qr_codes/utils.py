from urllib.parse import urljoin

import segno

from core.context_processors import server_url


def generate_qr_code(request, short_link):
    full_url = urljoin(server_url(request)["server_url"], short_link)
    return segno.make_qr(full_url)


__all__ = ["generate_qr_code"]
