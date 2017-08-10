#/bin/bash 

apt-get install -y postgresql postgresql-contrib python-virtualenv nginx supervisor

dfva_user_pass=`openssl rand -base64 16`

exc=`cat <<EOF
psql -c "CREATE USER dfva_user WITH PASSWORD '$dfva_user_pass';"
psql -c "CREATE DATABASE db_dfva;"
psql -c "grant all privileges on database db_dfva to dfva_user;"
EOF`

su - postgres -c "$exc"

groupadd --system webapps
useradd --system --gid webapps --shell /bin/bash --home /home/dfva dfva

mkdir -p /home/dfva
chown dfva:webapps /home/dfva

apt-get install -y git build-essential libssl-dev libffi-dev python3-dev libpq-dev


su - dfva -c "git clone https://github.com/luisza/dfva.git"
secret_key=`openssl rand -base64 32`

echo DBPASS="\"$dfva_user_pass\"" > /home/dfva/dfva/dfva/environment.py
echo -e "\n" >> /home/dfva/dfva/dfva/environment.py
echo SECRET_KEY ="\"$secret_key\"" >> /home/dfva/dfva/dfva/environment.py
echo "HOSTS =['dfva.info']" >> /home/dfva/dfva/dfva/environment.py

chown dfva:webapps /home/dfva/dfva/dfva/environment.py

su - dfva <<EOF
virtualenv -p python3 environment
source ~/environment/bin/activate
pip install --upgrade pip setuptools

cd dfva
pip install -r requirements.txt
pip install psycopg2 gunicorn 
mkdir -p /home/dfva/logs/
touch /home/dfva/logs/gunicorn_supervisor.log 

python manage.py migrate --settings=dfva.settings_prod
python manage.py collectstatic --settings=dfva.settings_prod

EOF

chmod u+x /home/dfva/dfva/deploy/gunicorn_start
cp /home/dfva/dfva/deploy/supervisor.conf /etc/supervisor/conf.d/

supervisorctl reread
supervisorctl update

cp /home/dfva/dfva/deploy/nginx.conf /etc/nginx/sites-available/dfva.conf
ln -s /etc/nginx/sites-available/dfva.conf /etc/nginx/sites-enabled/dfva.conf

service nginx restart 
apt-get remove -y git build-essential libssl-dev libffi-dev python3-dev libpq-dev
apt-get -y autoremove
