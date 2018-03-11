#!/bin/bash

if [ -z $CELERY ]; then
    bash /dfva_app/start_web.sh
else
    bash /dfva_app/start_worker.sh
fi
