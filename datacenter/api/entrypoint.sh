#!/usr/bin/env sh

CONTAINER_FIRST_STARTUP="CONTAINER_FIRST_STARTUP"
if [ ! -e /$CONTAINER_FIRST_STARTUP ]; then
    touch /$CONTAINER_FIRST_STARTUP
    flask --app app.main init-db
    gunicorn --config gunicorn-conf.py app.main:api
else
    gunicorn --config gunicorn-conf.py app.main:api
fi
