'''
Created on 13 sep. 2017

@author: luisza
'''
from rest_framework import serializers
from pyfva.clientes.validador import ClienteValidador
from django.utils.dateparse import parse_datetime
from pyfva.constants import get_text_representation, ERRORES_VALIDA_CERTIFICADO,\
    ERRORES_VALIDAR_XMLCOFIRMA, ERRORES_VALIDAR_ODF,\
    ERRORES_VALIDAR_XMLCONTRAFIRMA, ERRORES_VALIDAR_MSOFFICE
    
from corebase.models import Firmante, ErrorEncontrado, Advertencia
import logging
from django.core.exceptions import ValidationError
from pyfva.clientes.firmador import ClienteFirmador
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
        if self.requestdata['format']=='cofirma':
            dev = ERRORES_VALIDAR_XMLCOFIRMA
        elif self.requestdata['format']=='contrafirma':
            dev = ERRORES_VALIDAR_XMLCONTRAFIRMA
        elif self.requestdata['format']=='msoffice':
            dev = ERRORES_VALIDAR_MSOFFICE
        elif self.requestdata['format']=='odf':
            dev = ERRORES_VALIDAR_ODF
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
            if advertencia:
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
    
class ErrorEncontradoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ErrorEncontrado
        fields = ('codigo', 'detalle')


class FirmanteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Firmante
        fields = ('cedula', 'fecha_de_firma', 'nombre_completo')
