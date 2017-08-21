'''
Created on 20 jul. 2017

@author: luis
'''
# encoding: utf-8


from __future__ import unicode_literals

from django.utils.dateparse import parse_datetime
from rest_framework import serializers
from corebase.serializer import InstitutionBaseSerializer
import logging
import warnings
from validator.models import ValidateCertificateDataRequest,\
    ValidateCertificateRequest, ValidateDocumentRequest,\
    ValidateDocumentDataRequest, Advertencia, ErrorEncontrado, Firmante
from pyfva.clientes.validador import ClienteValidador
from rest_framework.exceptions import ValidationError
from pyfva.clientes.firmador import ClienteFirmador
from django.utils.translation import ugettext as _


# Person
from corebase.serializer import PersonBaseSerializer
from validator.models import ValidatePersonDocumentDataRequest, ValidatePersonDocumentRequest,\
    ValidatePersonCertificateDataRequest, ValidatePersonCertificateRequest
from pyfva.constants import get_text_representation, ERRORES_VALIDA_CERTIFICADO,\
    ERRORES_VALIDA_DOCUMENTO


logger = logging.getLogger('dfva')


class ValidateCertificate_RequestSerializer(serializers.HyperlinkedModelSerializer):
    data = serializers.CharField(
        help_text="""Datos de solicitud de validación de certificado encriptados usando 
        AES.MODE_EAX con la llave de sesión encriptada con PKCS1_OAEP
         """)
    readonly_fields = ['data']
    check_internal_fields = None

    validate_request_class = None
    validate_data_class = None

    def save_subject(self):
        pass

    def call_BCCR(self):
        client = ClienteValidador(
            negocio=self.institution.bccr_bussiness,
            entidad=self.institution.bccr_entity,
        )
        if client.validar_servicio('certificado'):

            data = client.validar_certificado_autenticacion(
                self.requestdata['document'])
            data['code'] = self.cert_request.code
        else:
            warnings.warn(
                _("Validate certificate BCCR not available"), RuntimeWarning)
            data = client.DEFAULT_CERTIFICATE_ERROR
            data['code'] = 'N/D'

        self.save_subject()
        self.adr.request_datetime = parse_datetime(
            self.requestdata['request_datetime'])
        self.adr.code = data['code']
        self.adr.status = data['codigo_error']
        if 'texto_codigo_error' in data:
            self.adr.status_text = data['texto_codigo_error']
        else:
            self.adr.status_text = get_text_representation(
                ERRORES_VALIDA_CERTIFICADO,  data['codigo_error'])
        self.adr.fue_exitosa = data['exitosa']

        if data['exitosa']:
            self.adr.identification = data['certificado']['identificacion']
            self.adr.nombre_completo = data['certificado']['nombre']
            self.adr.inicio_vigencia = data['certificado']['inicio_vigencia']
            self.adr.fin_vigencia = data['certificado']['fin_vigencia']

    def save(self, **kwargs):
        odata = {}
        for field in self.Meta.fields:
            if field == 'data':
                continue
            odata[field] = self.data[field]

        self.cert_request = self.validate_request_class(**odata)
        self.adr = self.validate_data_class()
        self.call_BCCR()
        self.adr.save()

        self.cert_request.data_request = self.adr
        self.cert_request.save()
        return self.cert_request


class ValidateCertificate_Request_Serializer(InstitutionBaseSerializer,
                                             ValidateCertificate_RequestSerializer):
    check_internal_fields = ['institution',
                             'notification_url',
                             'document',
                             'request_datetime']

    validate_request_class = ValidateCertificateRequest
    validate_data_class = ValidateCertificateDataRequest

    def save_subject(self):
        self.adr.notification_url = self.requestdata['notification_url']
        self.adr.institution = self.institution

    class Meta:
        model = ValidateCertificateRequest
        fields = ('institution', 'data_hash', 'algorithm',
                  'public_certificate', 'data')


class ValidateCertificateRequest_Response_Serializer(serializers.ModelSerializer):
    class Meta:
        model = ValidateCertificateDataRequest
        fields = ('identification', 'request_datetime',
                  'code', 'status', 'id_transaction',
                  'status_text', 'nombre_completo', 'inicio_vigencia', 'fin_vigencia',
                  'fue_exitosa')


class ValidateDocument_RequestSerializer(serializers.HyperlinkedModelSerializer):
    data = serializers.CharField(
        help_text="""Datos de solicitud de validación de certificado encriptados usando 
        AES.MODE_EAX con la llave de sesión encriptada con PKCS1_OAEP
         """)
    readonly_fields = ['data']
    check_internal_fields = None

    validate_request_class = None
    validate_data_class = None

    def save_subject(self):
        pass

    def call_BCCR(self):
        client = ClienteValidador(
            negocio=self.institution.bccr_bussiness,
            entidad=self.institution.bccr_entity,
        )
        if client.validar_servicio('documento'):

            data = client.validar_documento_xml(
                self.requestdata['document'])

        else:
            warnings.warn(
                _("Validate document BCCR not available"), RuntimeWarning)
            data = client.DEFAULT_DOCUMENT_ERROR

        self.save_subject()
        self.adr.request_datetime = parse_datetime(
            self.requestdata['request_datetime'])
        self.adr.code = self.document_request.code
        self.adr.status = data['codigo_error']
        if 'texto_codigo_error' in data:
            self.adr.status_text = data['texto_codigo_error']
        else:
            self.adr.status_text = get_text_representation(
                ERRORES_VALIDA_DOCUMENTO,  data['codigo_error'])
        self.adr.fue_exitosa = data['exitosa']

        self.adr.save()

        if data['exitosa']:
            self.get_advertencias(data['advertencias'])
            self.get_errores_encontrados(data['errores_encontrados'])
            self.get_firmantes(data['firmantes'])

    def get_firmantes(self, firmantes):
        if firmantes is None:
            return
        for firmante in firmantes:
            firmante = Firmante.objects.create(
                cedula=firmante['identificacion'],
                fecha_de_firma=firmante['fecha_firma'],
                nombre_completo=firmante['nombre']
            )
            self.adr.firmantes.add(firmante)

    def get_errores_encontrados(self, errores):
        if errores is None:
            return
        for error in errores:
            error, _ = ErrorEncontrado.objects.get_or_create(
                codigo=error[0],
                detalle=error[1]
            )
            self.adr.errores.add(error)

    def get_advertencias(self, advertencias):
        if advertencias is None:
            return
        for advertencia in advertencias:
            adv, _ = Advertencia.objects.get_or_create(
                descripcion=advertencia
            )
            self.adr.advertencias.add(adv)

    def save(self, **kwargs):
        odata = {}
        for field in self.Meta.fields:
            if field == 'data':
                continue
            odata[field] = self.data[field]

        self.document_request = self.validate_request_class(**odata)
        self.adr = self.validate_data_class()

        self.call_BCCR()
        self.adr.save()

        self.document_request.data_request = self.adr
        self.document_request.save()
        return self.document_request


class ErrorEncontradoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ErrorEncontrado
        fields = ('codigo', 'detalle')


class FirmanteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Firmante
        fields = ('cedula', 'fecha_de_firma', 'nombre_completo')


class ValidateDocument_ResponseSerializer(serializers.ModelSerializer):
    advertencias = serializers.StringRelatedField(many=True)
    firmantes = FirmanteSerializer(many=True)
    errores = ErrorEncontradoSerializer(many=True)


class ValidateDocumentRequest_Response_Serializer(ValidateDocument_ResponseSerializer):
    class Meta:
        model = ValidateDocumentDataRequest
        fields = ('request_datetime',
                  'code', 'status', 'status_text',
                  'advertencias', 'errores', 'firmantes',
                  'fue_exitosa')


class ValidateDocument_Request_Serializer(InstitutionBaseSerializer, ValidateDocument_RequestSerializer):
    check_internal_fields = ['institution',
                             'notification_url',
                             'document',
                             'request_datetime']

    validate_request_class = ValidateDocumentRequest
    validate_data_class = ValidateDocumentDataRequest

    def save_subject(self):
        self.adr.notification_url = self.requestdata['notification_url']
        self.adr.institution = self.institution

    class Meta:
        model = ValidateDocumentRequest
        fields = ('institution', 'data_hash', 'algorithm',
                  'public_certificate', 'data')


class ValidatePersonCertificate_Request_Serializer(PersonBaseSerializer, ValidateCertificate_RequestSerializer):
    check_internal_fields = ['person',
                             'document',
                             'request_datetime']

    validate_request_class = ValidatePersonCertificateRequest
    validate_data_class = ValidatePersonCertificateDataRequest

    def save_subject(self):
        self.adr.person = self.person

    class Meta:
        model = ValidatePersonCertificateRequest
        fields = ('person', 'data_hash', 'algorithm',
                  'public_certificate', 'data')


class ValidatePersonDocument_Request_Serializer(PersonBaseSerializer,
                                                ValidateDocument_RequestSerializer):
    check_internal_fields = ['person',
                             'document',
                             'request_datetime']

    validate_request_class = ValidatePersonDocumentRequest
    validate_data_class = ValidatePersonDocumentDataRequest

    def save_subject(self):
        self.adr.person = self.person

    class Meta:
        model = ValidatePersonDocumentRequest
        fields = ('person', 'data_hash', 'algorithm',
                  'public_certificate', 'data')


class ValidatePersonCertificateRequest_Response_Serializer(serializers.ModelSerializer):
    class Meta:
        model = ValidatePersonCertificateDataRequest
        fields = ('identification', 'request_datetime',
                  'code', 'status', 'status_text',
                  'nombre_completo', 'inicio_vigencia', 'fin_vigencia',
                  'fue_exitosa')


class ValidatePersonDocumentRequest_Response_Serializer(ValidateDocument_ResponseSerializer):
    class Meta:
        model = ValidatePersonDocumentDataRequest
        fields = ('request_datetime',
                  'code', 'status', 'status_text',
                  'advertencias', 'errores', 'firmantes',
                  'fue_exitosa')


class Suscriptor_Serializer(serializers.ModelSerializer):
    data = serializers.CharField(
        help_text="""Datos de solicitud de validación de certificado encriptados usando 
        AES.MODE_EAX con la llave de sesión encriptada con PKCS1_OAEP
         """)
    readonly_fields = ['data']

    def is_valid(self, raise_exception=False):
        serializers.Serializer.is_valid(
            self, raise_exception=raise_exception)
        self.validate_digest()
        self.validate_certificate()
        if self._errors and raise_exception:
            raise ValidationError(self.errors)
        return not bool(self._errors)

    def call_BCCR(self):
        signclient = ClienteFirmador(
            negocio=self.institution.bccr_bussiness,
            entidad=self.institution.bccr_entity,
        )
        if signclient.validar_servicio():

            data = signclient.suscriptor_conectado(
                self.requestdata['identification'])
        else:
            warnings.warn("Sign/Validate:  BCCR No disponible", RuntimeWarning)
            data = False
        return data

    def save(self, **kwargs):
        return self.call_BCCR()


class SuscriptorInstitution_Serializer(Suscriptor_Serializer, InstitutionBaseSerializer):
    check_internal_fields = ['institution',
                             'notification_url',
                             'identification',
                             'request_datetime']

    class Meta:
        model = ValidateDocumentRequest
        fields = ('institution', 'data_hash', 'algorithm',
                  'public_certificate', 'data')


class SuscriptorPerson_Serializer(Suscriptor_Serializer, PersonBaseSerializer):
    check_internal_fields = ['person',
                             'identification',
                             'request_datetime']

    class Meta:
        model = ValidatePersonDocumentRequest
        fields = ('person', 'data_hash', 'algorithm',
                  'public_certificate', 'data')
