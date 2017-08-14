# encoding: utf-8


'''
Created on 14/4/2017

@author: luisza
'''
from __future__ import unicode_literals

from django.utils import timezone
from django.utils.dateparse import parse_datetime
from rest_framework import serializers
from django.utils.translation import ugettext as _
from authenticator.models import AuthenticateDataRequest, AuthenticateRequest
import warnings
from pyfva.clientes.autenticador import ClienteAutenticador
from corebase.serializer import InstitutionCheckBaseBaseSerializer


# Person
from authenticator.models import AuthenticatePersonDataRequest, AuthenticatePersonRequest
from corebase.serializer import PersonCheckBaseBaseSerializer
from pyfva.constants import get_text_representation, ERRORES_AL_SOLICITAR_FIRMA


class Authenticate_RequestSerializer(serializers.HyperlinkedModelSerializer):
    data = serializers.CharField(
        help_text="""Datos de solicitud de autenticación encriptados usando 
        AES.MODE_EAX con la llave de sesión encriptada con PKCS1_OAEP
        """)
    readonly_fields = ['data']
    check_internal_fields = None

    validate_request_class = None
    validate_data_class = None

    def save_subject(self):
        pass

    def call_BCCR(self):
        authclient = ClienteAutenticador(self.institution.bccr_bussiness,
                                         self.institution.bccr_entity)
        if authclient.validar_servicio():
            data = authclient.solicitar_autenticacion(
                self.requestdata['identification'])

        else:
            warnings.warn(_("Auth BCCR not available"), RuntimeWarning)
            data = authclient.DEFAULT_ERROR

        self.save_subject()
        self.adr.institution = self.institution
        self.adr.request_datetime = parse_datetime(
            self.requestdata['request_datetime'])

        self.adr.expiration_datetime = timezone.now(
        ) + timezone.timedelta(minutes=data['tiempo_maximo'])
        self.adr.duration = data['tiempo_maximo']
        if 'texto_codigo_error' in data:
            self.adr.status_text = data['texto_codigo_error']
        else:
            self.adr.status_text = get_text_representation(
                ERRORES_AL_SOLICITAR_FIRMA,  data['codigo_error'])
        self.adr.status = data['codigo_error']
        self.adr.id_transaction = data['id_solicitud']
        self.adr.code = data['codigo_verificacion']

    def save(self, **kwargs):
        odata = {}
        for field in self.Meta.fields:
            if field == 'data':
                continue
            odata[field] = self.data[field]

        auth_request = self.validate_request_class(**odata)
        self.adr = self.validate_data_class()
        self.call_BCCR()
        self.adr.save()

        auth_request.data_request = self.adr
        auth_request.save()
        return auth_request


class Authenticate_Request_Serializer(InstitutionCheckBaseBaseSerializer, Authenticate_RequestSerializer):

    check_internal_fields = ['notification_url', 'identification',
                             'request_datetime', 'institution']

    check_show_fields = ['institution',
                         'notification_url',
                         'identification',
                         'request_datetime']

    validate_request_class = AuthenticateRequest
    validate_data_class = AuthenticateDataRequest

    def save_subject(self):
        self.adr.notification_url = self.requestdata['notification_url']
        self.adr.identification = self.requestdata['identification']

    class Meta:
        model = AuthenticateRequest
        fields = ('institution', 'data_hash', 'algorithm',
                  'public_certificate', 'data')


class Authenticate_Response_Serializer(serializers.ModelSerializer):

    class Meta:
        model = AuthenticateDataRequest
        fields = (
            'code', 'status', 'identification', 'id_transaction',
            'request_datetime', 'sign_document', 'expiration_datetime',
            'received_notification', 'duration', 'status_text')


class Authenticate_Person_Request_Serializer(PersonCheckBaseBaseSerializer, Authenticate_RequestSerializer):

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
