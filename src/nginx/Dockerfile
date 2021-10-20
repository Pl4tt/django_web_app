FROM nginx:latest

COPY ./default.conf etc/nginx/conf.d/default.conf
COPY ./uwsgi_params etc/nginx/uwsgi_params

USER root

RUN mkdir -p /vol/static/static && \
    mkdir -p /vol/static/media && \
    mkdir -p /vol/static/media/temp && \
    chmod 755 /vol/static
