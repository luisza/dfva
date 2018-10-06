'''
Created on 12 sep. 2017

@author: luisza
'''
# Person
from person.models import AuthenticatePersonRequest,\
    AuthenticatePersonDataRequest
from rest_framework import serializers
import logging
from corebase.authenticate import Authenticate_RequestSerializer
from person.serializer import PersonCheckBaseBaseSerializer
from django.conf import settings


logger = logging.getLogger(settings.DEFAULT_LOGGER_NAME)


class Authenticate_Person_Request_Serializer(PersonCheckBaseBaseSerializer,
                                             Authenticate_RequestSerializer):

    check_internal_fields = ['identification',
                             'request_datetime', 'person']
    check_show_fields = ['person',
                         'identification',
                         'request_datetime']
    validate_request_class = AuthenticatePersonRequest
    validate_data_class = AuthenticatePersonDataRequest

    def save_subject(self):
        self.adr.person = self.person
        self.adr.identification = self.requestdata['identification']

    class Meta:
        model = AuthenticatePersonRequest
        fields = ('person', 'data_hash', 'algorithm',
                  'public_certificate', 'data')


class Authenticate_Person_Response_Serializer(serializers.ModelSerializer):

    class Meta:
        model = AuthenticatePersonDataRequest
        fields = (
            'code', 'status', 'identification', 'id_transaction',
            'request_datetime', 'sign_document', 'expiration_datetime',
            'received_notification', 'duration', 'status_text')
