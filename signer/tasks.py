'''
Created on 11 sep. 2017

@author: luis
'''
import importlib
from django.conf import settings

app = importlib.import_module(settings.CELERY_MODULE).app
import logging

logger = logging.getLogger('dfva_sign')


@app.task
def remove_expired_signs():

    pass
