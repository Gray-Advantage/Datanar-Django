from datetime import datetime, timedelta
import re
from unittest.mock import patch

from allauth.account.models import EmailAddress
from django.core import mail
from django.shortcuts import reverse
from django.test import Client, override_settings, TestCase
from django.utils import timezone

from users.models import User


class ActivationTest(TestCase):
    def setUp(self):
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

    @override_settings(DEBUG=False, DEFAULT_USER_IS_ACTIVE=False)
    def test_activation_correct(self):
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

    @override_settings(DEBUG=False, DEFAULT_USER_IS_ACTIVE=False)
    @patch.object(timezone, "now")
    def test_activation_wrong(self, mock_now):
        future_time = timezone.make_aware(datetime.now() + timedelta(hours=13))
        mock_now.return_value = datetime.now()

        self.client.post(reverse("users:signup"), self.data)
        user = User.objects.get(username=self.data["username"])

        self.assertFalse(
            EmailAddress.objects.get_verified(user),
            "Неверное значение `verified` почты у `user`",
        )

        self.assertEqual(len(mail.outbox), 1, "Количество `mail.outbox` не 1")

        email_body = mail.outbox[0].body
        url = re.search(r"http://testserver(.+)", email_body).group(0)

        mock_now.return_value = future_time

        self.client.get(url)
        user = User.objects.get(username=self.data["username"])

        self.assertFalse(
            EmailAddress.objects.get_verified(user),
            "Неверное значение `verified` почты у `user`",
        )


__all__ = []
