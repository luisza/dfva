#!/bin/bash

docker-compose -f docker-compose-dev.yml exec  rabbitmq bash -c 'rabbitmqctl add_user dfva dfvapassword; rabbitmqctl add_vhost dfvavhost;rabbitmqctl set_user_tags dfva dfvatag; rabbitmqctl set_permissions -p dfvavhost dfva ".*" ".*" ".*"'
docker-compose -f docker-compose-dev.yml exec  rabbitmq bash -c 'rabbitmqctl add_user fvabccr fvabccrpassword; rabbitmqctl add_vhost fvabccrvhost;rabbitmqctl set_user_tags fvabccr fvabccrtag; rabbitmqctl set_permissions -p fvabccrvhost fvabccr ".*" ".*" ".*"'


docker-compose -f docker-compose-dev.yml exec  -u postgres   postgresdb bash -c "psql -v ON_ERROR_STOP=1 --username '$POSTGRES_USER' --dbname '$POSTGRES_DB' <<-EOSQL
    CREATE USER dfva WITH PASSWORD 'dfvapassword';
    CREATE USER fvabccr WITH PASSWORD 'fvabccrpassword';
    CREATE DATABASE dfva;
    CREATE DATABASE fvabccr;
    GRANT ALL PRIVILEGES ON DATABASE dfva TO dfva;
    GRANT ALL PRIVILEGES ON DATABASE fvabccr TO fvabccr;
EOSQL"

docker-compose -f docker-compose-dev.yml exec  dfva bash -c 'python manage.py migrate; python manage.py createsuperuser'
docker-compose -f docker-compose-dev.yml exec  dfva bash -c 'python manage.py crea_ca'
docker-compose -f docker-compose-dev.yml exec  fvabccr bash -c 'python fva_bccr/manage.py migrate; python fva_bccr/manage.py createsuperuser'