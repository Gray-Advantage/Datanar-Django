__all__ = ("clear_unconfirmed_users",)

from datetime import timedelta
from typing import Any

from allauth.account.models import EmailAddress
from celery.schedules import schedule
from django.conf import settings
from django.db.models import QuerySet
from django.utils import timezone

from datanar.celery import app
from redirects.models import Redirect
from users.models import User


def get_unconfirmed_users() -> QuerySet[User]:
    deadline = timezone.now() - timedelta(
        days=settings.UNCONFIRMED_USER_TTL_DAYS,
    )

    return (
        User.objects.filter(
            is_staff=False,
            is_superuser=False,
            last_login__isnull=True,
            date_joined__lt=deadline,
        )
        .exclude(
            pk__in=EmailAddress.objects.filter(verified=True).values(
                EmailAddress.user.field.name,
            ),
        )
        .exclude(
            pk__in=Redirect.objects.filter(user__isnull=False).values(
                Redirect.user.field.name,
            ),
        )
    )


@app.task()
def clear_unconfirmed_users() -> int:
    users = get_unconfirmed_users()
    count = users.count()
    users.delete()
    return count


@app.on_after_finalize.connect
def setup_periodic_tasks(sender: Any, **kwargs: Any) -> None:
    sender.add_periodic_task(
        schedule(run_every=timedelta(hours=1)),
        clear_unconfirmed_users,
    )
