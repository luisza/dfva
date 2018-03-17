'''
Created on 11 sep. 2017

@author: luis
'''
from __future__ import absolute_import

import os

from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', os.getenv('DJANGO_SETTINGS_MODULE', 'dfva.settings'))

from django.conf import settings  # noqa

if settings.DOCKER:
    RABBIT_USER = os.getenv('RABBIT_USER', 'guest')
    RABBIT_PASS = os.getenv('RABBIT_PASS', 'password')
    RABBIT_HOST = os.getenv('RABBIT_HOST', 'rabbitmq')
    RABBIT_PORT = os.getenv('RABBIT_PORT', '5672')
    app = Celery('dfva', broker='amqp://%s:%s@%s:%s'%(RABBIT_USER,RABBIT_PASS,RABBIT_HOST,RABBIT_PORT) ,backend='rpc://' )
else:
    app = Celery('dfva')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
