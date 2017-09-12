'''
Created on 11 sep. 2017

@author: luis
'''

import importlib
from django.conf import settings
#from django.core import serializers
from django.utils import timezone
from authenticator.models import AuthenticateDataRequest
from rest_framework import serializers
from rest_framework.renderers import JSONRenderer

app = importlib.import_module(settings.CELERY_MODULE).app
import logging
logger = logging.getLogger('dfva_authentication')


class LogAuthenticateInstitutionRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthenticateDataRequest
        fields = ('institution', 'notification_url', 'identification',
                  'request_datetime', 'code', 'status', 'status_text',
                  'response_datetime', 'expiration_datetime', 'id_transaction',
                  'duration', 'received_notification'
                  )


@app.task
def remove_expired_authentications():

    basetime = timezone.now() - timezone.timedelta(minutes=settings.DFVA_REMOVE_AUTHENTICATION)
    queryset = AuthenticateDataRequest.objects.filter(
        expiration_datetime__lte=basetime
    )
    if queryset.exists():
        data = LogAuthenticateInstitutionRequestSerializer(queryset, many=True)
        json = JSONRenderer().render(data.data).decode('utf-8')
        logger.info(json)
        queryset.delete()
