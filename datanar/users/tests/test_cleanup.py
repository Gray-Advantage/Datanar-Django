__all__ = ()

from datetime import timedelta

from allauth.account.models import EmailAddress
from django.test import override_settings, TestCase
from django.utils import timezone

from redirects.models import Redirect
from users import tasks
from users.models import User


@override_settings(UNCONFIRMED_USER_TTL_DAYS=1)
class ClearUnconfirmedUsersTest(TestCase):
    def make_user(self, username: str, joined_days_ago: int = 2) -> User:
        user = User.objects.create_user(
            username=username,
            email=f"{username}@email.com",
            password="some_password_123!",
        )
        User.objects.filter(pk=user.pk).update(
            date_joined=timezone.now() - timedelta(days=joined_days_ago),
        )
        user.refresh_from_db()
        return user

    def test_expired_unconfirmed_user_deleted(self) -> None:
        self.make_user("expired")

        self.assertEqual(
            tasks.clear_unconfirmed_users(),
            1,
            "Просроченный неподтверждённый `user` не удалён",
        )
        self.assertFalse(
            User.objects.filter(username="expired").exists(),
            "Просроченный неподтверждённый `user` остался в базе",
        )

    def test_fresh_user_kept(self) -> None:
        self.make_user("fresh", joined_days_ago=0)

        tasks.clear_unconfirmed_users()

        self.assertTrue(
            User.objects.filter(username="fresh").exists(),
            "`user` удалён до истечения срока подтверждения",
        )

    def test_verified_user_kept(self) -> None:
        user = self.make_user("verified")
        EmailAddress.objects.create(
            user=user,
            email=user.email,
            verified=True,
            primary=True,
        )

        tasks.clear_unconfirmed_users()

        self.assertTrue(
            User.objects.filter(username="verified").exists(),
            "`user` с подтверждённой почтой удалён",
        )

    def test_unverified_email_row_does_not_protect(self) -> None:
        user = self.make_user("unverified")
        EmailAddress.objects.create(
            user=user,
            email=user.email,
            verified=False,
            primary=True,
        )

        tasks.clear_unconfirmed_users()

        self.assertFalse(
            User.objects.filter(username="unverified").exists(),
            "`user` с неподтверждённой почтой не удалён",
        )

    def test_staff_kept(self) -> None:
        user = self.make_user("staff")
        user.is_staff = True
        user.save()

        tasks.clear_unconfirmed_users()

        self.assertTrue(
            User.objects.filter(username="staff").exists(),
            "`user` с `is_staff` удалён",
        )

    def test_superuser_kept(self) -> None:
        user = self.make_user("superuser")
        user.is_superuser = True
        user.save()

        tasks.clear_unconfirmed_users()

        self.assertTrue(
            User.objects.filter(username="superuser").exists(),
            "`user` с `is_superuser` удалён",
        )

    def test_logged_in_user_kept(self) -> None:
        user = self.make_user("logged_in")
        user.last_login = timezone.now()
        user.save()

        tasks.clear_unconfirmed_users()

        self.assertTrue(
            User.objects.filter(username="logged_in").exists(),
            "`user`, который хотя бы раз входил, удалён",
        )

    def test_user_with_redirects_kept(self) -> None:
        user = self.make_user("with_links")
        Redirect.objects.create(
            user=user,
            short_link="kept-link",
            long_link="https://www.python.org",
        )

        tasks.clear_unconfirmed_users()

        self.assertTrue(
            User.objects.filter(username="with_links").exists(),
            "`user` со ссылками удалён",
        )
        self.assertTrue(
            Redirect.objects.filter(short_link="kept-link").exists(),
            "Ссылка удалена вместе с `user`",
        )

    def test_only_expired_deleted_among_many(self) -> None:
        self.make_user("expired_one")
        self.make_user("expired_two")
        self.make_user("fresh_one", joined_days_ago=0)
        verified = self.make_user("verified_one")
        EmailAddress.objects.create(
            user=verified,
            email=verified.email,
            verified=True,
            primary=True,
        )

        self.assertEqual(
            tasks.clear_unconfirmed_users(),
            2,
            "Удалено не то количество `user`",
        )
        self.assertQuerySetEqual(
            User.objects.order_by("username").values_list(
                "username",
                flat=True,
            ),
            ["fresh_one", "verified_one"],
        )
