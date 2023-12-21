from pathlib import Path

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
import openpyxl

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
def create_redirects(data, user_id):
    links = get_links(data["links_file"])
    del data["links_file"]

    answer = []
    first = True
    second = True
    for long_link in links:
        data["long_link"] = long_link
        if first:
            data["custom_url"] = data["short_link"]
            first = False
        elif second:
            del data["custom_url"]
            second = False

        form = RedirectFormExtended(data)
        del form.cleaned_data["links_file"]

        redirect = Redirect.objects.create(**form.cleaned_data)
        redirect.user = User.objects.get(id=user_id)
        redirect.save()

        answer.append(redirect.short_link)

    return answer


__all__ = [create_redirects]
