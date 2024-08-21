from datetime import datetime, timedelta
from http import HTTPStatus
from unittest.mock import patch

from django.shortcuts import reverse
from django.test import Client, TestCase
from django.utils import timezone

from redirects import tasks
from redirects.models import Redirect


class RedirectionLifeCycle(TestCase):
    @patch.object(timezone, "now")
    def test_redirection_lifecycle(self, mock_now):
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
        self.assertQuerysetEqual(Redirect.objects.all(), [])

    @patch.object(timezone, "now")
    def test_redirection_lifecycle_with_celery_task(self, mock_now):
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
        self.assertQuerysetEqual(Redirect.objects.all(), [])


__all__ = []
