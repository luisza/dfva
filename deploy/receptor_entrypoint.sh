#!/bin/bash

# Prepare log files and start outputting logs to stdout
touch /logs/gunicorn.log
touch /logs/gunicorn-access.log
tail -n 0 -f /logs/gunicorn*.log &

echo "Esperando base de datos"
sleep 10
python manage.py migrate --settings=dfva.settings
python manage.py collectstatic --settings=dfva.settings --noinput

/usr/bin/update_crl.sh

export DJANGO_SETTINGS_MODULE=dfva.settings
service nginx start
service cron start

gunicorn dfva.wsgi:application \
    --name dfva --capture-output \
    --bind 127.0.0.1:8000 \
    --workers 3 \
    --log-level=info \
    --log-file=/logs/gunicorn.log \
    --access-logfile=/logs/gunicorn-access.log \
"$@" 

