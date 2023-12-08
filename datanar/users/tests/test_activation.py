from datetime import datetime, timedelta
import re
from unittest.mock import patch

from django.core import mail
from django.shortcuts import reverse
from django.test import Client, override_settings, TestCase
from django.utils import timezone

from users.models import User


class ActivationTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.data = {
            "username": "TestUser",
            "email": "test_user@email.com",
            "password1": "some_password_123!",
            "password2": "some_password_123!",
        }

    @override_settings(DEBUG=False, DEFAULT_USER_IS_ACTIVE=False)
    def test_activation_correct(self):
        self.client.post(reverse("users:signup"), self.data)
        user = User.objects.get(username=self.data["username"])

        self.assertFalse(
            user.is_active,
            "Неверное значение `is_active` у `user`",
        )

        self.assertEqual(len(mail.outbox), 1, "Количество `mail.outbox` не 1")

        email_body = mail.outbox[0].body
        url = re.search(r"http://testserver(.+)", email_body).group(0)

        self.client.get(url)
        user = User.objects.get(username=self.data["username"])

        self.assertTrue(
            user.is_active,
            "Неверное значение `is_active` у `user`",
        )

    @override_settings(DEBUG=False, DEFAULT_USER_IS_ACTIVE=False)
    @patch.object(timezone, "now")
    def test_activation_wrong(self, mock_now):
        future_time = timezone.make_aware(datetime.now() + timedelta(hours=13))
        mock_now.return_value = datetime.now()

        self.client.post(reverse("users:signup"), self.data)
        user = User.objects.get(username=self.data["username"])

        self.assertFalse(
            user.is_active,
            "Неверное значение `is_active` у `user`",
        )

        self.assertEqual(len(mail.outbox), 1, "Количество `mail.outbox` не 1")

        email_body = mail.outbox[0].body
        url = re.search(r"http://testserver(.+)", email_body).group(0)

        mock_now.return_value = future_time

        self.client.get(url)
        user = User.objects.get(username=self.data["username"])

        self.assertFalse(
            user.is_active,
            "Неверное значение `is_active` у `user`",
        )


__all__ = []
