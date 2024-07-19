FROM python:3.12.4-slim

RUN apt update
RUN apt install gettext -y

COPY ./requirements /requirements
RUN pip install -r requirements/prod.txt
RUN rm -rf requirements

COPY ./datanar /datanar/
WORKDIR /datanar

CMD python manage.py migrate \
 && python manage.py init_superuser \
 && python manage.py compilemessages \
 && python manage.py collectstatic --no-input \
 && python manage.py runserver 0.0.0.0:8000