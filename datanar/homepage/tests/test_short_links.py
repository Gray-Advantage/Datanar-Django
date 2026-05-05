from http import HTTPStatus

from django.shortcuts import reverse
from django.test import Client, TestCase
import parameterized

from redirects.forms import RedirectForm
from redirects.models import Redirect
from statistic.models import Click


class TestShortLinks(TestCase):
    def setUp(self):
        self.client = Client()
        self.form_data = {
            "long_link": "https://lyceum.yandex.ru/",
        }

    def test_diff_links(self):
        short_links = set()
        for i in range(15):
            self.client.post(reverse("homepage:home"), self.form_data)

            response = self.client.get(reverse("homepage:home"))
            messages = list(response.context["messages"])
            short_links.add(messages[0].message)

        self.assertEqual(len(short_links), 15, "Есть повторяющиеся ссылки")

    def test_create_redirect(self):
        redirect_count = Redirect.objects.count()

        self.client.post(
            reverse("homepage:home"),
            data=self.form_data,
            follow=True,
        )

        self.assertEqual(
            Redirect.objects.count(),
            redirect_count + 1,
            "Redirect не создан",
        )

        self.assertEqual(
            Redirect.objects.first().create_method,
            Redirect.CreateMethod.WEB,
            "Метод создания для `redirect` неправильный",
        )

    def test_redirect_short_link(self):
        response = self.client.post(
            reverse("homepage:home"),
            data=self.form_data,
            follow=True,
        )
        self.assertRedirects(response, reverse("homepage:home"))

        self.assertEqual(
            len(response.context["messages"]),
            1,
            "Нет `short_link`",
        )

    @parameterized.parameterized.expand(
        [
            "123abc4567",
            "vywrH82Kcd",
            "3P4esTIJIR",
            "pCpOMv7PVc",
            "xAJknNyfYf",
            "XDCvFMxvTk",
            "lzBupdSCxN",
            "gbai1hf3ce",
            "3fw81gbmw4",
            "frufve4t94",
        ],
    )
    def test_unknown_short_link_returns_404(self, unknown_short_links):
        response = self.client.get(
            reverse("redirects:redirect", args=[unknown_short_links]),
        )
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_redirects_with_correct_short_link(self):
        response = self.client.post(
            reverse("homepage:home"),
            data=self.form_data,
            follow=True,
        )
        self.assertRedirects(response, reverse("homepage:home"))

        messages = list(response.context["messages"])
        response = self.client.get(
            reverse("redirects:redirect", args=[messages[0].message]),
            follow=True,
        )
        self.assertRedirects(response, self.form_data["long_link"])

    @parameterized.parameterized.expand(
        [
            "test?",
            "test&",
            "test=",
            "test#",
            "test%",
            "test+",
            "test:",
            "test;",
            "test@",
            "test.test",
            "test test",
            "test,test",
            "test*test",
            "test(test)",
            "test)test",
            "test[test]",
            "test]test",
            "test{test}",
            "test}test",
            "test|test",
            "test\\test",
            ".",
            "..",
        ],
    )
    def test_redirects_with_incorrect_short_link(
        self,
        incorrect_short_link,
    ):
        response = self.client.post(
            reverse("homepage:home"),
            data=self.form_data | {"custom_url": incorrect_short_link},
        )
        self.assertIn("form", response.context)
        form: RedirectForm = response.context["form"]
        self.assertIn("custom_url", form.errors.keys())

    def test_create_click(self):
        click_count = Click.objects.count()
        response = self.client.post(
            reverse("homepage:home"),
            data=self.form_data,
            follow=True,
        )
        messages = list(response.context["messages"])
        self.client.get(
            reverse("redirects:redirect", args=[messages[0].message]),
        )
        self.assertEqual(
            Click.objects.count(),
            click_count + 1,
            "Click не создан",
        )


__all__ = []
