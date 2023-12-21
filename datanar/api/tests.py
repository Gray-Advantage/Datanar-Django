from django.test import Client, TestCase
from django.urls import reverse


class ApiContentTest(TestCase):
    fixtures = ["fixtures/data.json"]

    def setUp(self):
        self.username = "TestUser"
        self.password = "qscdewazx"
        self.client = Client()
        self.client.login(username=self.username, password=self.password)

    def test_new_token_context(self):
        client = Client()

        url = reverse("api:create_new_token")
        response1 = client.post(
            url,
            data={"username": self.username, "password": self.password},
        )
        response2 = client.post(
            url,
            data={"username": self.username, "password": self.password},
        )

        self.assertEqual(response1.status_code, 200)
        self.assertEqual(response2.status_code, 200)
        self.assertNotEquals(
            response1.json()["token"],
            response2.json()["token"],
        )

    def test_token_context(self):
        client = Client()

        url = reverse("api:get_token")
        response1 = client.post(
            url,
            data={"username": self.username, "password": self.password},
        )
        response2 = client.post(
            url,
            data={"username": self.username, "password": self.password},
        )

        self.assertEqual(response1.status_code, 200)
        self.assertEqual(response2.status_code, 200)
        self.assertEqual(response1.json()["token"], response2.json()["token"])

    def test_redirects_list(self):
        response = self.client.get(reverse("api:redirect-list"))
        self.assertEqual(response.status_code, 200)
        redirects_list = [
            redirect["short_link"] for redirect in response.json()
        ]
        self.assertEqual(
            redirects_list,
            [
                "short_AAA",
                "short_BBB",
                "short_CCC",
                "short_DDD",
                "short_EEE",
                "short_FFF",
            ],
        )

    def test_redirect_id(self):
        response = self.client.get(reverse("api:redirect-detail", args=[1]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["short_link"], "short_AAA")

    def test_create_redirect(self):
        response = self.client.post(
            reverse("api:redirect-list"),
            data={
                "long_link": "https://www.python.org/",
                "short_link": "test_short",
            },
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["short_link"], "test_short")

    def test_delete_redirect(self):
        response = self.client.delete(reverse("api:redirect-detail", args=[1]))
        self.assertEqual(response.status_code, 204)


__all__ = []
