'''
Created on 30 jul. 2017

@author: luis
'''
import requests
from authenticator.models import AuthenticateDataRequest
from authenticator.serializer import Authenticate_Response_Serializer
from signer.models import SignDataRequest
from signer.serializer import Sign_Response_Serializer
from rest_framework.renderers import JSONRenderer
from corebase.rsa import encrypt, get_hash_sum
import logging

logger = logging.getLogger('ucr_fva')


def get_datarequest_serializer(data):
    if isinstance(data, AuthenticateDataRequest):
        return Authenticate_Response_Serializer, data.authenticaterequest_set.first()
    elif isinstance(data, SignDataRequest):
        return Sign_Response_Serializer, data.signrequest_set.first()


def send_notification(data, serializer=None, request=None):

    if data.notification_url == 'N/D':
        return

    if serializer is None:
        serializer, req = get_datarequest_serializer(data)

    ars = serializer(data)
    datajson = JSONRenderer().render(ars.data)
    edata = encrypt(data.institution.public_key, datajson)
    hashsum = get_hash_sum(edata, req.algorithm)
    error = None
    try:
        response = requests.post(data.notification_url, data={'id_transaction': data.id_transaction,
                                                              'data': edata.decode(),
                                                              'hashsum': hashsum,
                                                              'algorithm': req.algorithm})
        response.raise_for_status()
    except Exception as e:
        error = e
        logger.error('Receptor: notificando a %s lanza %s' %
                     (data.notification_url, e))

    return error
