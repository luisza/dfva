'''
Created on 19 jul. 2017

@author: luis
'''
# encoding: utf-8


from __future__ import unicode_literals

from django.utils import timezone
from django.utils.dateparse import parse_datetime
from rest_framework import serializers
from corebase.serializer import CoreBaseBaseSerializer

import warnings
from signer.models import SignDataRequest, SignRequest, SignPersonDataRequest,\
    SignPersonRequest
from pyfva.clientes.firmador import ClienteFirmador


class Sign_RequestSerializer(CoreBaseBaseSerializer, serializers.HyperlinkedModelSerializer):

    data = serializers.CharField(
        help_text="""Datos de solicitud de autenticación encriptados usando 
        AES.MODE_EAX con la llave de sesión encriptada con PKCS1_OAEP
         """)
    readonly_fields = ['data']

    def save_subject(self):
        pass

    def call_BCCR(self):
        signclient = ClienteFirmador(
            negocio=self.institution.bccr_bussiness,
            entidad=self.institution.bccr_entity,
        )
        if signclient.validar_servicio():

            data = signclient.firme(
                self.requestdata['identification'],
                self.requestdata['document'],
                self.requestdata['format'],
                algoritmo_hash=self.requestdata['algorithm_hash'].title(),
                hash_doc=self.requestdata['document_hash'],
                resumen=self.requestdata['resumen'])

        else:
            warnings.warn("Sign BCCR No disponible", RuntimeWarning)
            data = signclient.DEFAULT_ERROR

        self.save_subject()
        self.adr.identification = self.requestdata['identification']
        self.adr.request_datetime = parse_datetime(
            self.requestdata['request_datetime'])

        self.adr.expiration_datetime = timezone.now(
        ) + timezone.timedelta(minutes=data['tiempo_maximo'])

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


class Sign_Request_Serializer(Sign_RequestSerializer):

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
                         'identification',
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


class Sign_Person_Request_Serializer(Sign_RequestSerializer):

    check_internal_fields = ['person',
                             'document',
                             'format',
                             'algorithm_hash',
                             'document_hash',
                             'resumen',
                             'identification',
                             'request_datetime']

    check_show_fields = ['person',
                         'identification',
                         'request_datetime']

    validate_request_class = SignPersonRequest
    validate_data_class = SignPersonDataRequest

    def save_subject(self):
        self.adr.person = self.person

    class Meta:
        model = SignPersonRequest
        fields = ('person', 'data_hash', 'algorithm',
                  'public_certificate', 'data')


class Sign_Response_Serializer(serializers.ModelSerializer):

    class Meta:
        model = SignDataRequest
        fields = (
            'code', 'status', 'identification', 'id_transaction',
            'sign_document',
            'request_datetime', 'expiration_datetime', 'received_notification')


class Sign_Person_Response_Serializer(serializers.ModelSerializer):

    class Meta:
        model = SignPersonDataRequest
        fields = (
            'code', 'status', 'identification', 'id_transaction',
            'sign_document',
            'request_datetime', 'expiration_datetime', 'received_notification')
