# Use an official Python runtime as a parent image
FROM python:3.6.4-stretch
ENV PYTHONUNBUFFERED 1

MAINTAINER Luis Zarate @luisza

RUN mkdir -p /dfva_app/
RUN mkdir -p /logs/
# Set the working directory to /app
WORKDIR /dfva_app

RUN apt-get update && \
    apt-get install -y  build-essential libssl1.1 libnss3 libssl-dev libffi-dev libnss3-dev
RUN pip install --trusted-host pypi.python.org --no-cache-dir  --upgrade pip && \
    pip install https://github.com/Solvosoft/soapfish/archive/v0.6.0.tar.gz
# Copy the current directory contents into the container at /app

COPY requirements.txt /dfva_app
COPY dogtag_requirements.txt  /dfva_app


# Install any needed packages specified in requirements.txt

RUN pip install --trusted-host pypi.python.org --no-cache-dir -r requirements.txt && \
    pip install --trusted-host pypi.python.org --no-cache-dir -r dogtag_requirements.txt
RUN apt-get remove -y  build-essential libssl-dev libffi-dev  libnss3-dev && \
    apt-get -y autoremove && \
    apt-get -y clean

ADD src /dfva_app 
RUN python manage.py collectstatic --settings=dfva.settings_docker
COPY deploy/docker_gunicorn.sh /entrypoint.sh
# EXPOSE port 8000 to allow communication to/from server
EXPOSE 8000

ENTRYPOINT ["/entrypoint.sh"]


