__all__ = ("RealIPMiddleware",)

from collections.abc import Callable
from ipaddress import ip_address, ip_network

from django.conf import settings
from django.http import HttpRequest, HttpResponse


class RealIPMiddleware:
    def __init__(
        self,
        get_response: Callable[[HttpRequest], HttpResponse],
    ) -> None:
        self.get_response = get_response
        self.trusted = [
            ip_network(network) for network in settings.TRUSTED_PROXIES
        ]

    def __call__(self, request: HttpRequest) -> HttpResponse:
        client_ip = self.get_client_ip(request)
        if client_ip is not None:
            request.META["REMOTE_ADDR"] = client_ip

        return self.get_response(request)

    def get_client_ip(self, request: HttpRequest) -> str | None:
        if not self.is_trusted(request.META.get("REMOTE_ADDR")):
            return None

        header = request.META.get(settings.REAL_IP_HEADER, "")
        return self.parse(header.split(",")[0].strip())

    def is_trusted(self, value: str | None) -> bool:
        parsed = self.parse(value)
        if parsed is None:
            return False

        address = ip_address(parsed)
        return any(address in network for network in self.trusted)

    @staticmethod
    def parse(value: str | None) -> str | None:
        if not value:
            return None

        try:
            return str(ip_address(value))
        except ValueError:
            return None
