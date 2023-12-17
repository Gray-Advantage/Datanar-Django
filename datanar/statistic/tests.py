from django.test import Client, TestCase
from django.urls import reverse


class ContextContentTest(TestCase):
    fixtures = ["fixtures/data.json"]

    def test_my_links_context(self):
        client = Client()
        client.login(username="bzorn", password="89884608152")
        url = reverse("statistic:my_links")
        response = client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context["messages"],
            [
                "tersf",
                "dfffdfdf",
                "fdsfsdf",
                "dfdfdfdfd",
                "fdfdfdfd",
                "ghghghghg",
            ],
        )


__all__ = []
