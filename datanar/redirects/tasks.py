from pathlib import Path
from urllib.parse import urlparse

from celery.schedules import schedule
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.db.models import DurationField, ExpressionWrapper, F, IntegerField
from django.utils import timezone
import openpyxl

from dashboard.models import BlockedDomain
from datanar.celery import app
from redirects.forms import RedirectFormExtended
from redirects.models import Redirect
from users.models import User

validator = URLValidator()


def get_from_txt(file_txt):
    answer = []
    for line in (x.lstrip().rstrip() for x in file_txt.readlines()):
        try:
            validator(line)
            if line.count("http:") > 1 or line.count("https:") > 1:
                raise ValidationError("")
            answer.append(line)
        except ValidationError:
            pass
    return answer


def get_from_xlsx(file_xlsx):
    workbook = openpyxl.load_workbook(file_xlsx.name)
    sheet = workbook.active
    answer = []
    for row in sheet.iter_rows(min_row=1, max_col=1, values_only=True):
        if row[0]:
            line = row[0].lstrip().rstrip()
            try:
                validator(line)
                if line.count("http:") > 1 or line.count("https:") > 1:
                    raise ValidationError("")
                answer.append(line)
            except ValidationError:
                pass
    return answer


def get_links(file_path):
    with Path(settings.MEDIA_ROOT / file_path).open() as file:
        file_extension = Path(file.name).suffix

        links = []
        if file_extension == ".txt":
            links = get_from_txt(file)
        elif file_extension == ".xlsx":
            links = get_from_xlsx(file)

    (settings.MEDIA_ROOT / file_path).unlink()
    return links  # noqa R504


@app.task()
def create_redirects(data, user_id, host, ip_address):
    links = get_links(data["links_file"])
    del data["links_file"]

    answer = []

    # Для первой ссылки используется custom_url, если есть, т.к. под капотом в
    # data custom_url превратилось в short_link, то указываем это явно
    first = True
    # Начиная с второго у нас нет custom_url, поэтому удаляем, чтобы short_link
    # генерировался сам
    second = True

    for long_link in links:
        if BlockedDomain.objects.is_blocked(long_link):
            continue

        data[Redirect.long_link.field.name] = long_link

        if first:
            data["custom_url"] = data[Redirect.short_link.field.name]
            first = False
        elif second:
            del data["custom_url"]
            second = False

        form = RedirectFormExtended(data)
        del form.cleaned_data["links_file"]

        url_long_link = urlparse(long_link)

        user_creator = User.objects.get(id=user_id)
        if url_long_link.netloc != host:
            redirect = Redirect.objects.create(**form.cleaned_data)
            redirect.create_method = Redirect.CreateMethod.WEB_FILE
            redirect.ip_address = ip_address
            redirect.user = user_creator
            redirect.save()
            short_link = redirect.short_link
        else:
            short_link = url_long_link.path

        answer.append(short_link)

    return answer


@app.task()
def clear_redirects():
    # Деактивация редиректов, чей срок годности истёк
    Redirect.objects.filter(
        is_active=True,
        validity_days__isnull=False,
    ).alias(
        time_since_creation=ExpressionWrapper(
            timezone.now() - F("created_at"),
            output_field=DurationField(),
        ),
    ).filter(
        time_since_creation__gt=ExpressionWrapper(
            F("validity_days") * 86400000000,  # перевод дней в микросекунды
            output_field=IntegerField(),
        ),
    ).update(
        is_active=False,
        deactivated_at=timezone.now(),
    )

    # Удаление деактивированных редиректов, чей срок больше 10 дней
    Redirect.objects.filter(
        is_active=False,
        deactivated_at__lt=timezone.now() - timezone.timedelta(days=10),
    ).delete()


@app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        schedule(run_every=40),
        clear_redirects,
    )


__all__ = [create_redirects, clear_redirects]
