'''
Created on 13 sep. 2017

@author: luisza
'''
from rest_framework import serializers
from pyfva.clientes.validador import ClienteValidador
from django.utils.dateparse import parse_datetime
from pyfva.constants import get_text_representation, ERRORES_VALIDA_CERTIFICADO,\
    ERRORES_VALIDAR_XMLCOFIRMA, ERRORES_VALIDAR_ODF,\
    ERRORES_VALIDAR_XMLCONTRAFIRMA, ERRORES_VALIDAR_MSOFFICE,\
    ERRORES_VALIDAR_PDF

from corebase.models import Signer, ErrorFound, WarningReceived
import logging
from django.core.exceptions import ValidationError
from pyfva.clientes.firmador import ClienteFirmador
logger = logging.getLogger('dfva')


def get_code_from_uuid(code):
    return str(code).split("-")[-1][:9]


class ValidateCertificate_RequestSerializer(
        serializers.HyperlinkedModelSerializer):
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
            data['code'] = get_code_from_uuid(self.cert_request.code)
        else:
            logger.warning("Validate certificate BCCR not available")
            data = client.DEFAULT_CERTIFICATE_ERROR
            data['code'] = 'N/D'

        logger.debug("Validator BCCR: certificate %r" % (data, ))
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
        self.adr.was_successfully = data['exitosa']

        if data['exitosa']:
            self.adr.identification = data['certificado']['identificacion']
            self.adr.full_name = data['certificado']['nombre']
            self.adr.start_validity = data['certificado']['inicio_vigencia']
            self.adr.end_validity = data['certificado']['fin_vigencia']

    def save(self, **kwargs):
        odata = {}
        for field in self.Meta.fields:
            if field == 'data':
                continue
            if field in self.data:
                odata[field] = self.data[field]

        self.cert_request = self.validate_request_class(**odata)
        self.adr = self.validate_data_class()
        self.call_BCCR()
        self.adr.save()

        self.cert_request.data_request = self.adr
        self.cert_request.save()
        return self.cert_request


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

    def get_default_error(self):
        dev = ERRORES_VALIDAR_XMLCOFIRMA
        if self.requestdata['format'] == 'cofirma':
            dev = ERRORES_VALIDAR_XMLCOFIRMA
        elif self.requestdata['format'] == 'contrafirma':
            dev = ERRORES_VALIDAR_XMLCONTRAFIRMA
        elif self.requestdata['format'] == 'msoffice':
            dev = ERRORES_VALIDAR_MSOFFICE
        elif self.requestdata['format'] == 'odf':
            dev = ERRORES_VALIDAR_ODF
        elif self.requestdata['format'] == 'pdf':
            dev = ERRORES_VALIDAR_PDF
        return dev

    def call_BCCR(self):
        client = ClienteValidador(
            negocio=self.institution.bccr_bussiness,
            entidad=self.institution.bccr_entity,
        )
        if client.validar_servicio('documento'):
            data = client.validar_documento(
                self.requestdata['document'], self.requestdata['format'])

        else:
            logger.warning("Validate document BCCR not available")
            data = client.DEFAULT_DOCUMENT_ERROR(self.get_default_error())

        logger.debug("Validator BCCR:  document %r" % (data, ))
        self.save_subject()
        self.adr.request_datetime = parse_datetime(
            self.requestdata['request_datetime'])
        self.adr.code = self.document_request.code
        self.adr.status = data['codigo_error']
        if 'texto_codigo_error' in data:
            self.adr.status_text = data['texto_codigo_error']
        else:
            self.adr.status_text = get_text_representation(
                self.get_default_error(),  data['codigo_error'])
        self.adr.was_successfully = data['exitosa']

        self.adr.save()

        if data['exitosa']:
            self.get_warnings(data['advertencias'])
            self.get_found_errors(data['errores_encontrados'])
            self.get_signers(data['firmantes'])

    def get_signers(self, signers):
        if signers is None:
            return
        for signer in signers:
            signerobj = Signer.objects.create(
                identification_number=signer['identificacion'],
                signature_date=signer['fecha_firma'],
                full_name=signer['nombre']
            )
            self.adr.signers.add(signerobj)

    def get_found_errors(self, errors):
        if errors is None:
            return
        for error in errors:
            error, _ = ErrorFound.objects.get_or_create(
                code=error[0],
                detail=error[1]
            )
            self.adr.errors.add(error)

    def get_warnings(self, warnings):
        if warnings is None:
            return
        for warning in warnings:
            if warning:
                adv, _ = WarningReceived.objects.get_or_create(
                    description=warning
                )
                self.adr.warnings.add(adv)

    def save(self, **kwargs):
        odata = {}
        for field in self.Meta.fields:
            if field == 'data':
                continue
            if field in self.data:
                odata[field] = self.data[field]

        self.document_request = self.validate_request_class(**odata)
        self.adr = self.validate_data_class()

        self.call_BCCR()
        self.adr.save()

        self.document_request.data_request = self.adr
        self.document_request.save()
        return self.document_request


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
            logger.warning("Sign/Validate:  BCCR No disponible")
            data = False
        logger.debug('Subscriptor %r' % (data,))
        return data

    def save(self, **kwargs):
        return self.call_BCCR()


class ErrorFoundSerializer(serializers.ModelSerializer):
    class Meta:
        model = ErrorFound
        fields = ('code', 'detail')


class SignerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Signer
        fields = ('identification_number',
                  'signature_date', 'full_name')
