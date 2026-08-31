__all__ = ("server_url",)

from django.http import HttpRequest


def server_url(request: HttpRequest) -> dict[str, str]:
    host = request.get_host()
    if "127.0.0.1" in host or "localhost" in host:
        return {"server_url": f"http://{host}"}
    return {"server_url": f"https://{host}"}
