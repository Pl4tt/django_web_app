FROM python:3.9.6

ENV PYTHONUNBUFFERED=1

WORKDIR /django

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

RUN mkdir -p /vol/static/static && \
    mkdir -p /vol/static/media && \
    mkdir -p /vol/static/temp && \
    chmod -R 755 /vol && \
    python manage.py collectstatic

USER root

