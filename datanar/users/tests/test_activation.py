__all__ = ()

import re

from allauth.account.models import EmailAddress
from django.core import mail
from django.test import Client, override_settings, TestCase
from django.urls import reverse

from users.models import User


class ActivationTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.data = {
            "username": "TestUser123",
            "email": "test_user123@email.com",
            "password1": "some_password_123!",
            "password2": "some_password_123!",
        }
        self.data1 = {
            "username": "TestUser321",
            "email": "test_user321@email.com",
            "password1": "some_password_123!",
            "password2": "some_password_123!",
        }

    @override_settings(ACCOUNT_EMAIL_VERIFICATION="mandatory")
    def test_activation_correct(self) -> None:
        self.client.post(reverse("users:signup"), self.data1)
        user = User.objects.get(username=self.data1["username"])

        self.assertFalse(
            EmailAddress.objects.get_verified(user),
            "Неверное значение `verified` почты у `user`",
        )

        self.assertEqual(len(mail.outbox), 1, "Количество `mail.outbox` не 1")

        email_body = mail.outbox[0].body
        url = re.search(r"http://testserver(.+)", email_body).group(0)

        self.client.post(url)
        user = User.objects.get(username=self.data1["username"])

        self.assertTrue(
            bool(EmailAddress.objects.get_verified(user)),
            "Неверное значение `verified` почты у `user`",
        )

    @override_settings(ACCOUNT_EMAIL_VERIFICATION="mandatory")
    def test_activation_wrong(self) -> None:
        self.client.post(reverse("users:signup"), self.data)
        user = User.objects.get(username=self.data["username"])

        self.assertFalse(
            EmailAddress.objects.get_verified(user),
            "Неверное значение `verified` почты у `user`",
        )

        self.assertEqual(len(mail.outbox), 1, "Количество `mail.outbox` не 1")

        email_body = mail.outbox[0].body
        url = re.search(r"http://testserver(.+)", email_body).group(0)

        with override_settings(ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS=0):
            self.client.post(url)

        user = User.objects.get(username=self.data["username"])

        self.assertFalse(
            EmailAddress.objects.get_verified(user),
            "Протухшая ссылка подтвердила почту у `user`",
        )
