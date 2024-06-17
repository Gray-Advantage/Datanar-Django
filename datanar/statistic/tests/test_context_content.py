from django.test import Client, TestCase
from django.urls import reverse


class ContextContentTest(TestCase):
    fixtures = ["fixtures/data.json"]

    def test_my_links_context(self):
        client = Client()
        client.login(username="TestUser", password="qscdewazx")

        url = reverse("statistic:my_links")
        response = client.get(url)

        self.assertEqual(response.status_code, 200)

        self.assertQuerysetEqual(
            response.context["links"],
            [
                "short_FFF",
                "short_EEE",
                "short_DDD",
                "short_CCC",
                "short_BBB",
                "short_AAA",
            ],
        )


__all__ = []
