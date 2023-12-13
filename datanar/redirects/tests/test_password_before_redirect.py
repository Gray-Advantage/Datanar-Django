from django.shortcuts import reverse
from django.test import Client, TestCase

from redirects.forms import PasswordForm
from redirects.models import Redirect


class PasswordBeforeRedirectTest(TestCase):
    def test_redirect_without_password(self):
        Redirect.objects.create(
            **{
                "long_link": "https://lyceum.yandex.ru/",
                "short_link": "custom",
            },
        )

        response = Client().get(reverse("redirects:redirect", args=["custom"]))
        self.assertRedirects(
            response,
            "https://lyceum.yandex.ru/",
            msg_prefix="Перенаправление не произошло",
        )

    def test_redirect_with_password(self):
        Redirect.objects.create(
            **{
                "long_link": "https://lyceum.yandex.ru/",
                "short_link": "secret",
                "password": "123",
            },
        )

        response = Client().get(reverse("redirects:redirect", args=["secret"]))
        self.assertNotEqual(
            response.status_code,
            302,
            "Ссылка с паролем делает редирект",
        )

        response = Client().post(
            reverse("redirects:redirect", args=["secret"]),
            {"password": "123"},
        )
        self.assertRedirects(
            response,
            "https://lyceum.yandex.ru/",
            msg_prefix="Перенаправление не произошло",
        )

    def test_password_form_before_redirect(self):
        Redirect.objects.create(
            **{
                "long_link": "https://lyceum.yandex.ru/",
                "short_link": "secret",
                "password": "123",
            },
        )

        response = Client().get(reverse("redirects:redirect", args=["secret"]))
        self.assertIn("form", response.context, "Нет `form` в контексте")
        self.assertIsInstance(
            response.context["form"],
            PasswordForm,
            "Загружена не верная форма",
        )

        response = Client().post(
            reverse("redirects:redirect", args=["secret"]),
            {"password": "not correct password"},
        )

        self.assertIn(
            "password",
            response.context["form"].errors,
            "Ошибка пароля не вызвана",
        )

        response = Client().post(
            reverse("redirects:redirect", args=["secret"]),
            {"password": "123"},
        )
        self.assertRedirects(
            response,
            "https://lyceum.yandex.ru/",
            msg_prefix="Перенаправление не произошло",
        )


__all__ = []
