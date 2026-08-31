__all__ = ()

from datetime import datetime, timedelta
from http import HTTPStatus
from unittest.mock import MagicMock, patch

from django.test import Client, TestCase
from django.urls import reverse
from django.utils import timezone

from redirects import tasks
from redirects.models import Redirect


class RedirectionLifeCycle(TestCase):
    @patch.object(timezone, "now")
    def test_redirection_lifecycle(self, mock_now: MagicMock) -> None:
        future_time = timezone.make_aware(
            datetime.now()
            + timedelta(
                days=Redirect.validity_days.field.default,
                seconds=1,
            ),
        )
        mock_now.return_value = timezone.make_aware(datetime.now())

        Client().post(
            reverse("homepage:home"),
            data={"long_link": "https://www.python.org"},
        )  # Создали redirect, получаем short_link
        short_link = Redirect.objects.first().short_link

        response = Client().get(
            reverse("redirects:redirect", args=[short_link]),
        )  # Проверяем, что работает сейчас
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(Redirect.objects.first().is_active, True)

        mock_now.return_value = future_time

        response = Client().get(
            reverse("redirects:redirect", args=[short_link]),
        )  # Проверяем, что произошла деактивация после срока годности
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertEqual(Redirect.objects.first().is_active, False)
        self.assertEqual(Redirect.objects.first().deactivated_at, future_time)

        mock_now.return_value += timedelta(days=10, seconds=1)

        response = Client().get(
            reverse("redirects:redirect", args=[short_link]),
        )  # Проверяем, что произошло удаление деактивированной ссылки
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertQuerySetEqual(Redirect.objects.all(), [])

    @patch.object(timezone, "now")
    def test_redirection_lifecycle_with_celery_task(
        self,
        mock_now: MagicMock,
    ) -> None:
        mock_now.return_value = timezone.make_aware(datetime.now())

        Client().post(
            reverse("homepage:home"),
            data={"long_link": "https://www.python.org"},
        )  # Создали redirect

        tasks.clear_redirects()
        self.assertEqual(Redirect.objects.first().is_active, True)

        mock_now.return_value += timedelta(
            days=Redirect.validity_days.field.default,
            seconds=1,
        )

        tasks.clear_redirects()
        self.assertEqual(Redirect.objects.first().is_active, False)

        mock_now.return_value += timedelta(days=10, seconds=1)

        tasks.clear_redirects()
        self.assertQuerySetEqual(Redirect.objects.all(), [])
