from django.test import Client, TestCase
from django.urls import reverse
from rest_framework import status


class ApiCorrectTest(TestCase):
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

    def test_new_token_context(self):
        client = Client()

        response1 = client.post(
            reverse("api:create_new_token"),
            data={"username": self.username, "password": self.password},
        )
        self.assertEqual(response1.status_code, status.HTTP_200_OK)

        response2 = client.post(
            reverse("api:create_new_token"),
            data={"username": self.username, "password": self.password},
        )
        self.assertEqual(response2.status_code, status.HTTP_200_OK)

        self.assertNotEqual(
            response1.json()["token"],
            response2.json()["token"],
        )

    def test_token_context(self):
        response1 = Client().post(
            reverse("api:get_token"),
            data={"username": self.username, "password": self.password},
        )
        self.assertEqual(response1.status_code, status.HTTP_200_OK)

        response2 = Client().post(
            reverse("api:get_token"),
            data={"username": self.username, "password": self.password},
        )
        self.assertEqual(response2.status_code, status.HTTP_200_OK)

        self.assertEqual(response1.json()["token"], response2.json()["token"])

    def test_redirects_list(self):
        response = self.client.get(reverse("api:redirect-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(
            [redirect["short_link"] for redirect in response.json()],
            self.short_links,
        )

    def test_redirect_id(self):
        for i in range(1, 7):
            response = self.client.get(
                reverse("api:redirect-detail", args=[i]),
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(
                response.json()["short_link"],
                self.short_links[i - 1],
            )

    def test_create_redirect(self):
        response = self.client.post(
            reverse("api:redirect-list"),
            data={"long_link": "https://python.org/"},
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()["long_link"], "https://python.org/")

        response = self.client.get(
            reverse(
                "redirects:redirect",
                args=[response.json()["short_link"]],
            ),
            follow=True,
        )
        self.assertRedirects(response, "https://python.org/")

    def test_create_redirect_with_short_link(self):
        response = self.client.post(
            reverse("api:redirect-list"),
            data={
                "long_link": "https://python.org/",
                "short_link": "test_short",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()["long_link"], "https://python.org/")
        self.assertEqual(response.json()["short_link"], "test_short")

    def test_delete_redirect(self):
        response = self.client.delete(reverse("api:redirect-detail", args=[1]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


__all__ = []
