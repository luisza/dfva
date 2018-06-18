'''
Created on 12 sep. 2017

@author: luisza
'''
import logging
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from rest_framework import serializers
from pyfva.clientes.firmador import ClienteFirmador

logger = logging.getLogger('dfva')


class Sign_RequestSerializer(serializers.HyperlinkedModelSerializer):

    data = serializers.CharField(
        help_text="""Datos de solicitud de autenticación encriptados usando 
        AES.MODE_EAX con la llave de sesión encriptada con PKCS1_OAEP
         """)
    readonly_fields = ['data']

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
            logger.warning("Sign BCCR not available")
            data = signclient.DEFAULT_ERROR

        logger.debug("Sign BCCR: %r" % (data, ))
        self.save_subject()
        self.adr.identification = self.requestdata['identification']
        self.adr.request_datetime = parse_datetime(
            self.requestdata['request_datetime'])
        self.adr.duration = data['tiempo_maximo']
        if 'texto_codigo_error' in data:
            self.adr.status_text = data['texto_codigo_error']
        self.adr.expiration_datetime = timezone.now(
        ) + timezone.timedelta(minutes=data['tiempo_maximo'])

        self.adr.status = data['codigo_error']
        self.adr.id_transaction = data['id_solicitud']
        self.adr.code = data['codigo_verificacion']
        self.adr.document_format = self.requestdata['format']

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
