'''
Created on 12 sep. 2017

@author: luisza
'''
import logging
from corebase.signer import Sign_RequestSerializer
from institution.models import SignRequest, SignDataRequest
from rest_framework import serializers
from institution.serializer import InstitutionCheckBaseBaseSerializer

logger = logging.getLogger('dfva')


class Sign_Request_Serializer(InstitutionCheckBaseBaseSerializer, Sign_RequestSerializer):

    check_internal_fields = ['institution',
                             'notification_url',
                             'document',
                             'format',
                             'algorithm_hash',
                             'document_hash',
                             'resumen',
                             'identification',
                             'request_datetime']
    check_show_fields = ['institution',
                         'notification_url',
                         #'identification',
                         'request_datetime']

    validate_request_class = SignRequest
    validate_data_class = SignDataRequest

    def save_subject(self):
        self.adr.notification_url = self.requestdata['notification_url']
        self.adr.institution = self.institution

    class Meta:
        model = SignRequest
        fields = ('institution', 'data_hash', 'algorithm',
                  'public_certificate', 'data')


class Sign_Response_Serializer(serializers.ModelSerializer):
    class Meta:
        model = SignDataRequest
        fields = (
            'code', 'status', 'identification', 'id_transaction',
            'sign_document', 'duration', 'status_text',
            'request_datetime', 'expiration_datetime', 'received_notification')


class LogSingInstitutionRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = SignDataRequest
        fields = (
            'institution', 'notification_url', 'identification',
            'request_datetime', 'code', 'status', 'status_text',
            'response_datetime', 'expiration_datetime', 'id_transaction',
            'duration', 'received_notification'
        )
