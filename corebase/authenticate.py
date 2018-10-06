'''
Created on 12 sep. 2017

@author: luisza
'''
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from rest_framework import serializers
from pyfva.clientes.autenticador import ClienteAutenticador
from pyfva.constants import get_text_representation, ERRORES_AL_SOLICITAR_FIRMA
from django.conf import settings
import logging

logger = logging.getLogger(settings.DEFAULT_LOGGER_NAME)


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
            logger.warning("Auth BCCR not available")
            data = authclient.DEFAULT_ERROR

        logger.debug("Authentication BCCR: %r" % (data, ))
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
            if field in self.data:
                odata[field] = self.data[field]

        auth_request = self.validate_request_class(**odata)
        self.adr = self.validate_data_class()
        self.call_BCCR()
        self.adr.save()

        auth_request.data_request = self.adr
        auth_request.save()
        return auth_request
