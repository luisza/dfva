apt-get install -y postgresql postgresql-contrib

fdva_user_pass=$(openssl rand -base64 16)

su - postgres
psql -c "CREATE USER dfva_user WITH PASSWORD '$dfva_user_pass';"
psql -c "CREATE DATABASE db_dfva;"
psql -c "grant all privileges on database db_dfva to dfva_user;"
logout

groupadd --system webapps
useradd --system --gid webapps --shell /bin/bash --home /home/dfva dfva
apt-get install -y python-virtualenv git

mkdir -p /home/dfva
chown dfva:webapps /home/dfva

apt-get install -y build-essential libssl-dev libffi-dev python3-dev libpq-dev

su - dfva
virtualenv -p python3 environment
source ~/environment/bin/activate
pip install --upgrade pip setuptools

git clone https://github.com/luisza/dfva.git
cd dfva
pip install -r requirements.txt
pip install psycopg2 gunicorn 

cd dfva
secret_key=$(openssl rand -base64 32)
echo -e "DBPASS='$dfva_user_pass'\n" >> environment.py
echo -e "SECRET_KEY = '$secret_key'\n" >> environment.py
logout

chmod u+x /home/dfva/dfva/deploy/gunicorn_start



apt-get remove -y git build-essential libssl-dev libffi-dev python3-dev libpq-dev
