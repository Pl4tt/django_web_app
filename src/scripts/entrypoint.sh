#!/bin/sh

set -e

uwsgi --socket :8000 --master --enable-threads --workers 4 --module web_app.wsgi