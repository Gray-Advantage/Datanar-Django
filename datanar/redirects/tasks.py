from datetime import timedelta
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


def is_line_valid(line: str) -> bool:
    try:
        validator(line)
        if line.count("http:") > 1 or line.count("https:") > 1:
            raise ValidationError
    except ValidationError:
        return False
    return True


def get_from_txt(file_txt):
    lines = (x.strip() for x in file_txt)
    return list(filter(is_line_valid, lines))


def get_from_xlsx(file_xlsx):
    workbook = openpyxl.load_workbook(file_xlsx.name)
    sheet = workbook.active

    lines = (
        row[0].strip()
        for row in sheet.iter_rows(min_row=1, max_col=1, values_only=True)
        if row[0]
    )
    return list(filter(is_line_valid, lines))


def get_links(file_path):
    with Path(settings.MEDIA_ROOT / file_path).open() as file:
        file_extension = Path(file.name).suffix

        links = []
        if file_extension == ".txt":
            links = get_from_txt(file)
        elif file_extension == ".xlsx":
            links = get_from_xlsx(file)

    (settings.MEDIA_ROOT / file_path).unlink()
    return links


@app.task()
def create_redirects(data, user_id, host, ip_address):
    file_field_name = "links_file"
    links = get_links(data.pop(file_field_name))

    answer = []

    try:
        user_creator = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return answer

    # Для первой ссылки используется short_link, если он есть.
    # Начиная с второй у нас нет short_link,
    # поэтому удаляем его, чтобы генерировался сам.

    for i, long_link in enumerate(links):
        if BlockedDomain.objects.is_blocked(long_link):
            continue

        data[Redirect.long_link.field.name] = long_link

        if i == 1:
            data.pop(Redirect.short_link.field.name)

        form = RedirectFormExtended(data)
        del form.cleaned_data[file_field_name]

        url_long_link = urlparse(long_link)

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
    redirect = Redirect.objects.filter(
        is_active=True,
        validity_days__isnull=False,
    )
    if settings.USE_FILE_DATABASE:  # SQLITE3
        redirect = redirect.alias(
            time_since_creation=ExpressionWrapper(
                timezone.now() - F(Redirect.created_at.field.name),
                output_field=DurationField(),
            ),
        ).filter(
            time_since_creation__gt=ExpressionWrapper(
                F(Redirect.validity_days.field.name)
                * 86400000000,  # перевод дней в микросекунды
                output_field=IntegerField(),
            ),
        )
    else:  # POSTGRES
        redirect = redirect.filter(
            created_at__lt=ExpressionWrapper(
                timezone.now()
                - F(Redirect.validity_days.field.name) * timedelta(days=1),
                output_field=DurationField(),
            ),
        )

    redirect.update(
        is_active=False,
        deactivated_at=timezone.now(),
    )

    # Удаление деактивированных редиректов, чей срок больше 10 дней
    Redirect.objects.filter(
        is_active=False,
        deactivated_at__lt=timezone.now() - timedelta(days=10),
    ).delete()


@app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        schedule(run_every=10),
        clear_redirects,
    )


__all__ = ["clear_redirects", "create_redirects"]
