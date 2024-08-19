from django.test import Client, TestCase
from django.urls import reverse
from rest_framework import status

from redirects.models import Redirect


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
        self.full_redirect_fields = {
            "id",
            "long_link",
            "short_link",
            "password",
            "validity_days",
            "validity_clicks",
            "created_at",
            "create_method",
            "is_active",
            "deactivated_at",
        }
        self.simple_redirect_fields = {
            "long_link",
            "short_link",
            "password",
            "validity_days",
            "validity_clicks",
            "created_at",
        }

    def test_create_new_token_context(self):
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

    def test_get_token_context(self):
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

    def test_get_redirects_list(self):
        response = self.client.get(reverse("api:redirect-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(
            [redirect["short_link"] for redirect in response.json()],
            self.short_links,
        )

    def test_get_redirects_list_context(self):
        response = self.client.get(reverse("api:redirect-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        for redirect in response.json():
            self.assertEqual(
                redirect.keys(),
                self.full_redirect_fields,
                "Отсутствует обязательное для авторизированного клиента поле",
            )

    def test_redirect_id(self):
        for i in range(1, len(self.short_links) + 1):
            response = self.client.get(
                reverse("api:redirect-detail", args=[i]),
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(
                response.json()["short_link"],
                self.short_links[i - 1],
            )

    def test_redirect_id_context(self):
        for i in range(1, len(self.short_links) + 1):
            response = self.client.get(
                reverse("api:redirect-detail", args=[i]),
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(
                response.json().keys(),
                self.full_redirect_fields,
                "Отсутствует обязательное для авторизированного клиента поле",
            )

    def test_create_redirect(self):
        redirect_count = Redirect.objects.count()

        response = self.client.post(
            reverse("api:redirect-list"),
            data={"long_link": "https://python.org/"},
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()["long_link"], "https://python.org/")

        self.assertEqual(
            Redirect.objects.count(),
            redirect_count + 1,
            "Redirect не создан",
        )

        self.assertEqual(
            Redirect.objects.last().create_method,
            Redirect.CreateMethod.API,
            "Метод создания для `redirect` неправильный",
        )

        response = self.client.get(
            reverse(
                "redirects:redirect",
                args=[response.json()["short_link"]],
            ),
            follow=True,
        )
        self.assertRedirects(response, "https://python.org/")

    def test_create_redirect_context(self):
        response = Client().post(
            reverse("api:redirect-list"),
            data={"long_link": "https://python.org/"},
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            response.json().keys(),
            self.simple_redirect_fields,
            "Присутствуют лишние поля для не авторизированного пользователя",
        )

        token = Client().post(
            reverse("api:get_token"),
            data={"username": self.username, "password": self.password},
        ).json()["token"]
        response = self.client.post(
            reverse("api:redirect-list"),
            data={"token": token, "long_link": "https://python.org/"},
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            response.json().keys(),
            self.full_redirect_fields,
            "Отсутствует обязательное для авторизированного пользователя поле",
        )

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
        redirect_count = Redirect.objects.count()

        response = self.client.delete(reverse("api:redirect-detail", args=[1]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertEqual(
            Redirect.objects.count(),
            redirect_count - 1,
            "Redirect не удалён",
        )


__all__ = []
