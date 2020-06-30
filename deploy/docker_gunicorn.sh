#!/bin/bash

# Prepare log files and start outputting logs to stdout
touch /logs/gunicorn.log
touch /logs/gunicorn-access.log
tail -n 0 -f /logs/gunicorn*.log &

echo "Esperando base de datos"
sleep 10
python manage.py migrate --settings=dfva.settings

export DJANGO_SETTINGS_MODULE=dfva.settings

gunicorn dfva.wsgi:application \
    --name dfva \
    --bind 0.0.0.0:8000 \
    --workers 3 \
    --log-level=info \
    --log-file=/logs/gunicorn.log \
    --access-logfile=/logs/gunicorn-access.log \
"$@"
