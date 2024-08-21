from django.shortcuts import reverse
from django.test import Client, override_settings, TestCase
from django.utils import timezone

from redirects.forms import RedirectForm, RedirectFormExtended
from redirects.models import Redirect
from users.models import User


class RedirectFormTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user_data = {
            "username": "TestUser",
            "email": "test_user@email.com",
            "password1": "some_password_123!",
            "password2": "some_password_123!",
        }
        self.form_data = {
            "long_link": "https://lyceum.yandex.ru/",
            "password": "qwerty",
            "validity_days": 130,
            "validity_clicks": 42,
        }

    @override_settings(DEFAULT_USER_IS_ACTIVE=True)
    def test_redirect_form_without_auth_user(self):
        response = self.client.get(reverse("homepage:home"))
        self.assertIn("form", response.context_data, "Нет `form` в контексте")
        self.assertIsInstance(
            response.context_data["form"],
            RedirectForm,
            "`form` не является `RedirectForm`",
        )

    @override_settings(DEFAULT_USER_IS_ACTIVE=True)
    def test_redirect_form_with_auth_user(self):
        self.client.post(reverse("users:signup"), self.user_data)
        self.client.login(
            username=self.user_data["username"],
            password=self.user_data["password1"],
        )

        response = self.client.get(reverse("homepage:home"))
        self.assertIn("form", response.context_data, "Нет `form` в контексте")
        self.assertIsInstance(
            response.context_data["form"],
            RedirectFormExtended,
            "`form` не расширена для зарегистрированного пользователя",
        )

    def test_extend_data_do_not_save_without_auth_user(self):
        self.client.post(reverse("homepage:home"), data=self.form_data)

        redirect = Redirect.objects.all().first()

        form_data = self.form_data.copy()
        form_data.update(
            {
                "user": None,
                "password": None,
                "validity_clicks": None,
                "validity_days": Redirect.validity_days.field.default,
            },
        )

        for field_name, field_value in form_data.items():
            self.assertEqual(
                eval(f"redirect.{field_name}", {"redirect": redirect}),
                field_value,
                f"`{field_name}` в `redirect` не значение по умолчанию",
            )

    @override_settings(DEFAULT_USER_IS_ACTIVE=True)
    def test_extend_data_save_with_auth_user(self):
        self.client.post(reverse("users:signup"), self.user_data)
        self.client.login(
            username=self.user_data["username"],
            password=self.user_data["password1"],
        )
        user = User.objects.get(username=self.user_data["username"])

        data = self.form_data.copy()
        data["date_validity_field"] = (
            timezone.now() + timezone.timedelta(days=data["validity_days"])
        ).date()
        del data["validity_days"]
        self.client.post(reverse("homepage:home"), data=data)

        redirect = Redirect.objects.all().first()

        form_data = self.form_data.copy()
        form_data.update({"user": user})

        for field_name, field_value in form_data.items():
            self.assertEqual(
                eval(f"redirect.{field_name}", {"redirect": redirect}),
                field_value,
                f"`{field_name}` не сохранён в `redirect`",
            )


__all__ = []
