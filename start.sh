#!/bin/bash

# Collect static files
echo "Collect static files"
python manage.py collectstatic --settings=dfva.settings_docker --noinput

echo "Waiting for db"
sleep 3

# Apply database migrations
echo "Apply database migrations"
python manage.py migrate --settings=dfva.settings_docker


python manage.py shell --settings=dfva.settings_docker <<< `cat <<EOF
from django.contrib.auth.models import User;
user=User.objects.create_user('$ADMIN_USER', password='$ADMIN_PASS');
user.is_superuser=True;
user.is_staff=True;
user.save()
EOF`


# Start server
echo "Starting server"
export DOCKER=True
# Start Gunicorn processes
echo Starting Gunicorn.
exec gunicorn dfva.wsgi_docker:application \
    --bind 0.0.0.0:8000 \
    --workers 1 &

exec celery -A dfva worker -l info -B

