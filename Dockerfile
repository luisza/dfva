# Use an official Python runtime as a parent image
FROM python:3.6.4-stretch
ENV PYTHONUNBUFFERED 1
RUN mkdir -p /dfva/logs/
# Set the working directory to /app
WORKDIR /dfva_app
# Copy the current directory contents into the container at /app
ADD . /dfva_app
ADD requirements.txt /dfva_app
ADD requirements/dogtag_requirements.txt  /dfva_app
# Install any needed packages specified in requirements.txt
RUN apt-get update
RUN apt-get install -y  build-essential libssl-dev libffi-dev libnss3-dev
RUN pip install https://github.com/luisza/soapfish/archive/v0.5.2.tar.gz
RUN pip install --trusted-host pypi.python.org --no-cache-dir -r requirements.txt
RUN pip install --trusted-host pypi.python.org --no-cache-dir -r dogtag_requirements.txt
RUN apt-get remove -y  build-essential libssl-dev libffi-dev  libnss3-dev
RUN apt-get -y autoremove
RUN apt-get -y clean

RUN python manage.py collectstatic --settings=dfva.settings_docker

# EXPOSE port 8000 to allow communication to/from server
EXPOSE 443


