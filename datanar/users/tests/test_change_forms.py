import re

from django.core import mail
from django.shortcuts import reverse
from django.test import Client, override_settings, TestCase

from users.models import User


class ChangeFormTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.data = {
            "username": "TestUser12345",
            "email": "testuser54321@email.com",
            "password1": "some_password_123!",
            "password2": "some_password_123!",
        }
        self.data1 = {
            "username": "TestUser54321",
            "email": "testuser12345@email.com",
            "password1": "some_password_54321!",
            "password2": "some_password_54321!",
        }

    @override_settings(ACCOUNT_EMAIL_VERIFICATION="none")
    def test_change_login(self):
        self.client.post(reverse("users:signup"), self.data1)
        self.client.login(
            username=self.data1["username"],
            password=self.data1["password1"],
        )
        user1 = User.objects.get(username=self.data1["username"])
        old_login = user1.username

        self.client.post(
            reverse("users:profile"),
            {"username": self.data["username"]},
        )
        user = User.objects.get(username=self.data["username"])
        new_login = user.username

        self.assertEqual(user1, user)
        self.assertNotEqual(old_login, new_login)

    @override_settings(ACCOUNT_EMAIL_VERIFICATION="none")
    def test_change_password(self):
        self.client.post(reverse("users:signup"), self.data1)
        self.client.login(
            username=self.data1["username"],
            password=self.data1["password1"],
        )
        user1 = User.objects.get(username=self.data1["username"])
        old_password = user1.password

        self.client.post(
            reverse("users:password_change"),
            {
                "oldpassword": self.data1["password1"],
                "password1": self.data["password1"],
                "password2": self.data["password1"],
            },
        )
        user = User.objects.get(username=self.data1["username"])
        new_password = user.password

        self.assertEqual(user1, user)
        self.assertNotEqual(old_password, new_password)

    @override_settings(ACCOUNT_EMAIL_VERIFICATION="mandatory")
    def test_change_email(self):
        self.client.post(reverse("users:signup"), self.data)
        email_body = mail.outbox[0].body
        url = re.search(r"http://testserver(.+)", email_body).group(0)
        self.client.post(url)
        self.client.login(
            username=self.data["username"],
            password=self.data["password1"],
        )
        user1 = User.objects.get(username=self.data["username"])
        old_email = user1.email

        self.client.post(
            reverse("users:email_change"),
            {"email": "exampleac@yandex.ru", "action_add": True},
            follow=True,
        )
        email_body = mail.outbox[1].body
        url = re.search(r"http://testserver(.+)", email_body).group(0)
        self.client.post(url)
        user = User.objects.get(username=self.data["username"])
        new_email = user.email

        self.assertEqual(user1, user)
        self.assertNotEqual(old_email, new_email)


__all__ = []
