# Use an official Python runtime as a parent image
FROM python:3.6.4-stretch
ENV PYTHONUNBUFFERED 1

MAINTAINER Luis Zarate @luisza

RUN mkdir -p /dfva_app/
RUN mkdir -p /logs/
# Set the working directory to /app
WORKDIR /dfva_app


# Copy the current directory contents into the container at /app
ADD src /dfva_app 
COPY requirements.txt /dfva_app
COPY dogtag_requirements.txt  /dfva_app
COPY deploy/docker_gunicorn.sh /entrypoint.sh

# Install any needed packages specified in requirements.txt
RUN apt-get update
RUN apt-get install -y  build-essential libssl1.1 libnss3 libssl-dev libffi-dev libnss3-dev
RUN pip install --trusted-host pypi.python.org --no-cache-dir  --upgrade pip
RUN pip install https://github.com/Solvosoft/soapfish/archive/v0.6.0.tar.gz
RUN pip install --trusted-host pypi.python.org --no-cache-dir -r requirements.txt
RUN pip install --trusted-host pypi.python.org --no-cache-dir -r dogtag_requirements.txt
RUN pip install python-logstash django-elasticsearch-dsl 'elasticsearch-dsl>=5.0,<6.0'
RUN apt-get remove -y  build-essential libssl-dev libffi-dev  libnss3-dev
RUN apt-get -y autoremove
RUN apt-get -y clean

RUN python manage.py collectstatic --settings=dfva.settings_docker

# EXPOSE port 8000 to allow communication to/from server
EXPOSE 8000

ENTRYPOINT ["/entrypoint.sh"]


