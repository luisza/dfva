#!/bin/bash

# Prepare log files and start outputting logs to stdout
touch /logs/gunicorn.log
touch /logs/gunicorn-access.log
tail -n 0 -f /logs/gunicorn*.log &

export DJANGO_SETTINGS_MODULE=dfva.settings_docker

exec gunicorn dfva.wsgi_docker:application \
    --name dfva \
    --bind 0.0.0.0:8000 \
    --workers 5 \
    --log-level=info \
    --log-file=/logs/gunicorn.log \
    --access-logfile=/logs/gunicorn-access.log \
"$@"
