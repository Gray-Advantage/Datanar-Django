from datetime import datetime
from unittest.mock import patch

from django.test import Client, TestCase
from django.urls import reverse
from django.utils import timezone
from rest_framework import status


class ApiWrongTest(TestCase):
    fixtures = ["fixtures/for_test_data.json"]

    def setUp(self):
        self.username = "TestUser"
        self.password = "qscdewazx"
        self.client = Client()
        self.client.login(username=self.username, password=self.password)
        self.short_links = [
            "short_AAA",
            "short_BBB",
            "short_CCC",
            "short_DDD",
            "short_EEE",
            "short_FFF",
        ]

    def test_new_token_with_wrong_auth_data(self):
        client = Client()

        response_1 = client.post(
            reverse("api:create_new_token"),
            data={"username": self.username + "_w", "password": self.password},
        )
        self.assertEqual(response_1.status_code, status.HTTP_400_BAD_REQUEST)

        response_2 = client.post(
            reverse("api:create_new_token"),
            data={"username": self.username, "password": self.password + "_w"},
        )
        self.assertEqual(response_2.status_code, status.HTTP_400_BAD_REQUEST)

    def test_redirect_without_auth(self):
        response = Client().get(reverse("api:redirect-detail", args=[1]))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_redirect_with_wrong_token(self):
        token = self.client.post(
            reverse("api:get_token"),
            data={"username": self.username, "password": self.password},
        ).json()["token"]

        response = Client().get(
            reverse("api:redirect-detail", args=[1]),
            data={"token": token + "_w"},
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_redirect_with_wrong_id(self):
        response = self.client.get(reverse("api:redirect-detail", args=[42]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        response = self.client.get(reverse("api:redirect-detail", args=["37"]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        for elem in [-1, 0, -100, "abc", "3!4", "56#"]:
            response = self.client.get(
                reverse("api:redirect-detail", args=[elem]),
            )
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch.object(timezone, "now")
    def test_create_redirect_with_wrong_data(self, mock_now):
        mock_now.return_value = timezone.make_aware(datetime(2023, 12, 30))

        for data, error in [
            ({}, status.HTTP_400_BAD_REQUEST),
            ({"long_link": "not utl"}, status.HTTP_400_BAD_REQUEST),
            ({"long_link": "https://example.com/"}, status.HTTP_423_LOCKED),
            (
                {
                    "long_link": "https://example.com",
                    "short_link": self.short_links[0],
                },
                status.HTTP_409_CONFLICT,
            ),
        ]:
            response = Client().post(reverse("api:redirect-list"), data=data)
            self.assertEqual(response.status_code, error)

    def test_create_redirect_with_wrong_auth(self):
        for add_data in [
            {"password": "qwerty"},
            {"validity_days": 200},
            {"validity_clicks": 100},
        ]:
            res = Client().post(
                reverse("api:redirect-list"),
                data={"long_link": "https://python.org/", **add_data},
            )
            self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_redirect_with_wrong_data(self):
        response = self.client.delete(
            reverse("api:redirect-detail", args=[42]),
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        response = self.client.delete(
            reverse("api:redirect-detail", args=["37"]),
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        for elem in [-1, 0, -100, "abc", "3!4", "56#"]:
            response = self.client.delete(
                reverse("api:redirect-detail", args=[elem]),
            )
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


__all__ = []
