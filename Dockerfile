# Use an official Python runtime as a parent image
FROM python:3.7-buster
ENV PYTHONUNBUFFERED 1

MAINTAINER Luis Zarate @luisza

RUN mkdir -p /dfva_app/
RUN mkdir -p /logs/
RUN mkdir -p /certs/
# Set the working directory to /app
WORKDIR /dfva_app

RUN apt-get update && \
    apt-get install -y  build-essential libssl1.1 libnss3 libssl-dev libffi-dev libnss3-dev
RUN pip install --trusted-host pypi.python.org --no-cache-dir  --upgrade pip && \
    pip install soapfish2==0.7.1
# Copy the current directory contents into the container at /app

COPY requirements.txt /dfva_app
COPY dogtag_requirements.txt  /dfva_app


# Install any needed packages specified in requirements.txt

RUN pip install --trusted-host pypi.python.org --no-cache-dir -r requirements.txt && \
    pip install --trusted-host pypi.python.org --no-cache-dir -r dogtag_requirements.txt && \
    pip install python-logstash django-elasticsearch-dsl 'elasticsearch-dsl>=5.0,<6.0'
RUN apt-get remove -y  build-essential libssl-dev libffi-dev  libnss3-dev && \
    apt-get -y autoremove && \
    apt-get -y clean

ADD src /dfva_app 
RUN python manage.py collectstatic --settings=dfva.settings
COPY deploy/docker_gunicorn.sh /entrypoint.sh
# EXPOSE port 8000 to allow communication to/from server
EXPOSE 8000

RUN mkdir -p /internal_ca
VOLUME /internal_ca
ENTRYPOINT ["/entrypoint.sh"]


