#!/bin/bash



# Start server
echo "Starting server"
export DOCKER=True
exec celery -A dfva worker -l info -B

