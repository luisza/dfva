'''
Created on 12 sep. 2017

@author: luisza
'''


import logging
from institution.models import AuthenticateRequest, AuthenticateDataRequest
from corebase.authenticate import Authenticate_RequestSerializer
from rest_framework import serializers
from institution.serializer import InstitutionCheckBaseBaseSerializer
from django.conf import settings

logger = logging.getLogger(settings.DEFAULT_LOGGER_NAME)


class Authenticate_Request_Serializer(InstitutionCheckBaseBaseSerializer,
                                      Authenticate_RequestSerializer):

    check_internal_fields = ['notification_url', 'identification',
                             'request_datetime', 'institution']

    check_show_fields = ['institution',
                         'notification_url',
                         # 'identification',
                         'request_datetime']

    validate_request_class = AuthenticateRequest
    validate_data_class = AuthenticateDataRequest

    def save_subject(self):
        self.adr.notification_url = self.requestdata['notification_url']
        self.adr.identification = self.requestdata['identification']

    class Meta:
        model = AuthenticateRequest
        fields = ('institution', 'data_hash', 'algorithm',
                  'public_certificate', 'data', 'encrypt_method')


class Authenticate_Response_Serializer(serializers.ModelSerializer):

    class Meta:
        model = AuthenticateDataRequest
        fields = (
            'code', 'status', 'identification', 'id_transaction',
            'request_datetime', 'sign_document', 'expiration_datetime',
            'received_notification', 'duration', 'status_text')


class LogAuthenticateInstitutionRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthenticateDataRequest
        fields = ('institution', 'notification_url', 'identification',
                  'request_datetime', 'code', 'status', 'status_text',
                  'response_datetime', 'expiration_datetime', 'id_transaction',
                  'duration', 'received_notification'
                  )
