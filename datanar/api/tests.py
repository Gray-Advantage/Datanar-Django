from django.test import Client, TestCase
from django.urls import reverse


class ApiContentTest(TestCase):
    fixtures = ["fixtures/data.json"]

    def test_new_token_context(self):
        username = "TestUser"
        password = "qscdewazx"
        client = Client()

        url = reverse("api:create_new_token")
        response1 = client.post(url, data={"username": username, "password": password})
        response2 = client.post(url, data={"username": username, "password": password})

        self.assertEqual(response1.status_code, 200)
        self.assertEqual(response2.status_code, 200)
        self.assertNotEquals(response1.json()['token'], response2.json()['token'])

    def test_token_context(self):
        username = "TestUser"
        password = "qscdewazx"
        client = Client()

        url = reverse("api:get_token")
        response1 = client.post(url, data={"username": username, "password": password})
        response2 = client.post(url, data={"username": username, "password": password})

        self.assertEqual(response1.status_code, 200)
        self.assertEqual(response2.status_code, 200)
        self.assertEqual(response1.json()['token'], response2.json()['token'])


__all__ = []
