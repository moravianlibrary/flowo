FROM  python:3.10-slim-bullseye

ENV PYTHONUNBUFFERED=1

RUN pip install django django-cors-headers

RUN pip install Django Celery djangorestframework django-cors-headers djangorestframework-simplejwt parsel requests


COPY ./api/ /api/
COPY ./flowo/ /flowo/
COPY ./manage.py .

EXPOSE 8000