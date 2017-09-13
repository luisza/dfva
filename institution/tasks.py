'''
Created on 12 sep. 2017

@author: luisza
'''
import importlib
from django.conf import settings
from django.utils import timezone
from rest_framework.renderers import JSONRenderer
from institution.models import AuthenticateDataRequest, SignDataRequest
from institution.authenticator.serializer import LogAuthenticateInstitutionRequestSerializer
from institution.signer.serializer import LogSingInstitutionRequestSerializer

app = importlib.import_module(settings.CELERY_MODULE).app
import logging
logger_auth = logging.getLogger('dfva_authentication')
logger_sign = logging.getLogger('dfva_sign')

@app.task
def remove_expired_authentications():

    basetime = timezone.now() - timezone.timedelta(minutes=settings.DFVA_REMOVE_AUTHENTICATION)
    queryset = AuthenticateDataRequest.objects.filter(
        expiration_datetime__lte=basetime
    )
    if queryset.exists():
        data = LogAuthenticateInstitutionRequestSerializer(queryset, many=True)
        json = JSONRenderer().render(data.data).decode('utf-8')
        logger_auth.info(json)
        queryset.delete()



@app.task
def remove_expired_signs():
    basetime = timezone.now() - timezone.timedelta(minutes=settings.DFVA_REMOVE_SIGN)
    queryset = SignDataRequest.objects.filter(
        expiration_datetime__lte=basetime
    )

    if queryset.exists():
        data = LogSingInstitutionRequestSerializer(queryset, many=True)
        json = JSONRenderer().render(data.data).decode('utf-8')
        logger_sign.info(json)
        queryset.delete()
