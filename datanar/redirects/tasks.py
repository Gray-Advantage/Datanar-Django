from pathlib import Path

from django.conf import settings

from datanar.celery import app
from redirects.forms import RedirectForm
from redirects.models import Redirect
from users.models import User


def get_from_txt(file_txt):
    return [line.rstrip() for line in file_txt.readlines() if line]


def get_from_xlsx(file_xlsx):
    return []


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
        form = RedirectForm(data)
        redirect = Redirect.objects.create(**form.cleaned_data)
        redirect.user = User.objects.get(id=user_id)
        redirect.save()
        answer.append(redirect.short_link)

    return answer


__all__ = [create_redirects]
