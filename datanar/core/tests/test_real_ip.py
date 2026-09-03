__all__ = ()

from http import HTTPStatus

from django.core.cache import cache
from django.test import Client, override_settings, TestCase
from django.urls import reverse


@override_settings(
    TRUSTED_PROXIES=["172.16.0.0/12"],
    REAL_IP_HEADER="HTTP_X_REAL_IP",
)
class RealIPMiddlewareTest(TestCase):
    def remote_addr(self, **extra: str) -> str:
        response = Client().get(reverse("homepage:home"), **extra)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        return response.wsgi_request.META["REMOTE_ADDR"]

    def test_replaced_behind_trusted_proxy(self) -> None:
        self.assertEqual(
            self.remote_addr(
                REMOTE_ADDR="172.18.0.5",
                HTTP_X_REAL_IP="203.0.113.7",
            ),
            "203.0.113.7",
            "`REMOTE_ADDR` не заменён адресом клиента от доверенного прокси",
        )

    def test_kept_when_proxy_is_not_trusted(self) -> None:
        self.assertEqual(
            self.remote_addr(
                REMOTE_ADDR="203.0.113.1",
                HTTP_X_REAL_IP="198.51.100.9",
            ),
            "203.0.113.1",
            "`REMOTE_ADDR` заменён по заголовку от недоверенного адреса",
        )

    def test_kept_without_header(self) -> None:
        self.assertEqual(
            self.remote_addr(REMOTE_ADDR="172.18.0.5"),
            "172.18.0.5",
            "`REMOTE_ADDR` изменён без заголовка с адресом клиента",
        )

    def test_broken_header_ignored(self) -> None:
        self.assertEqual(
            self.remote_addr(
                REMOTE_ADDR="172.18.0.5",
                HTTP_X_REAL_IP="not-an-ip",
            ),
            "172.18.0.5",
            "`REMOTE_ADDR` заменён мусором из заголовка",
        )

    def test_first_address_of_list_taken(self) -> None:
        self.assertEqual(
            self.remote_addr(
                REMOTE_ADDR="172.18.0.5",
                HTTP_X_REAL_IP="203.0.113.7, 172.18.0.5",
            ),
            "203.0.113.7",
            "Из списка адресов взят не первый",
        )

    @override_settings(TRUSTED_PROXIES=[])
    def test_disabled_by_empty_trusted_proxies(self) -> None:
        self.assertEqual(
            self.remote_addr(
                REMOTE_ADDR="172.18.0.5",
                HTTP_X_REAL_IP="203.0.113.7",
            ),
            "172.18.0.5",
            "`REMOTE_ADDR` заменён при пустом `TRUSTED_PROXIES`",
        )


@override_settings(
    TRUSTED_PROXIES=["172.16.0.0/12"],
    ACCOUNT_RATE_LIMITS={"signup": "3/300s/ip"},
    PASSWORD_HASHERS=["django.contrib.auth.hashers.MD5PasswordHasher"],
)
class SignupRateLimitTest(TestCase):
    def setUp(self) -> None:
        cache.clear()

    def signup(self, real_ip: str, count: int) -> list[int]:
        codes = []
        for i in range(count):
            name = f"user{real_ip.replace('.', '')}{i}"
            response = Client().post(
                reverse("users:signup"),
                {
                    "username": name,
                    "email": f"{name}@email.com",
                    "password1": "some_password_123!",
                    "password2": "some_password_123!",
                },
                REMOTE_ADDR="172.18.0.5",
                HTTP_X_REAL_IP=real_ip,
            )
            codes.append(response.status_code)

        return codes

    def test_limit_applies_per_client_ip(self) -> None:
        self.assertEqual(
            self.signup("203.0.113.7", 5),
            [
                HTTPStatus.FOUND,
                HTTPStatus.FOUND,
                HTTPStatus.FOUND,
                HTTPStatus.TOO_MANY_REQUESTS,
                HTTPStatus.TOO_MANY_REQUESTS,
            ],
            "Лимит регистраций не сработал на адресе клиента",
        )

    def test_limit_does_not_leak_between_clients(self) -> None:
        self.signup("203.0.113.7", 5)

        self.assertEqual(
            self.signup("198.51.100.9", 2),
            [HTTPStatus.FOUND, HTTPStatus.FOUND],
            "Лимит одного клиента задел другого",
        )
