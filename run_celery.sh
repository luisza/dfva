#!/bin/bash

[[ "$@" =~ '-nup' ]] && nup=true

if [ !nup ]; then
docker run -d --rm --name dfva-mail -p 8025:8025 -p  1025:1025 -d mailhog/mailhog
docker run -d --rm --name dfva-rabbitmq -p 5672:5672 -d rabbitmq:3
fi

echo "Esperando el inicio de rabbitmq ..." && sleep 20


cd src/
celery worker -A dfva -l info -B
#--scheduler django_celery_beat.schedulers:DatabaseScheduler

if [ !nup ]; then
docker rm -f dfva-mail
docker rm -f dfva-rabbitmq
fi