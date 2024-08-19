from http import HTTPStatus

from django.test import Client, TestCase
from django.urls import reverse


class QRCodeWrongTest(TestCase):
    def test_wrong_types(self):
        for type_ in ["PNG", "html", "123", "%1", "gif"]:
            response = Client().get(
                reverse("qr_code:download", args=[type_, "12345"]),
            )
            self.assertEqual(
                response.status_code,
                HTTPStatus.UNSUPPORTED_MEDIA_TYPE,
            )
            self.assertEqual(response.content, b"")

    def test_without_necessary_data(self):
        response = Client().get(
            reverse("qr_code:download", args=["png", "1"])[:-3],  # удалить /1/
        )
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

        response = Client().get(
            reverse("qr_code:download", args=["png", "1"])[:-2] + "/",
        )
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)


__all__ = []
