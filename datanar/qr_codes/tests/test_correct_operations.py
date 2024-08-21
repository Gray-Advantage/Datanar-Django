from http import HTTPStatus

from django.test import Client, TestCase
from django.urls import reverse


class QRCodeCorrectTest(TestCase):
    def test_correct_data(self):
        for type_ in ["png", "jpg", "svg"]:
            response = Client().get(
                reverse("qr_code:download", args=[type_, "12345"]),
            )
            self.assertEqual(response.status_code, HTTPStatus.OK)
            self.assertNotEqual(response.content, b"")


__all__ = []
