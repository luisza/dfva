# encoding: utf-8

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

'''
@date: 12/9/2017
@author: Luis Zarate Montero
@contact: luis.zarate@solvosoft.com
@license: GPLv3
'''
import uuid

from django.utils import timezone

from corebase.models import Signer, ErrorFound, WarningReceived
from corebase.time import parse_datetime
from institution.models import Institution
from person.models import ValidatePersonDocumentRequest,\
    ValidatePersonCertificateRequest
from institution.validator.serializer import \
    ValidateDocument_ResponseSerializer

from rest_framework import serializers
from corebase.validator import ValidateDocument_RequestSerializer,\
    ValidateCertificate_RequestSerializer, Suscriptor_Serializer
from person.serializer import PersonBaseSerializer
from pyfva.constants import get_text_representation, \
    ERRORES_VALIDA_CERTIFICADO,\
    ERRORES_VALIDAR_XMLCOFIRMA, ERRORES_VALIDAR_ODF,\
    ERRORES_VALIDAR_XMLCONTRAFIRMA, ERRORES_VALIDAR_MSOFFICE,\
    ERRORES_VALIDAR_PDF
from pyfva.clientes.validador import ClienteValidador
from pyfva.clientes.firmador import ClienteFirmador

from corebase import logger
from django.conf import settings

RESPONSE_CERTIFICATE_FIELDS = ('status', 'status_text', 'was_successfully', 'identification', 'full_name', 'start_validity', 'end_validity' )

def get_code_from_uuid(code):
    """
    Genera un código como el del BCCR basado en un código UUID

    :param code: str - UUID pa calcularle el code
    :return: str - código semejante al BCCR
    """
    return str(code).split("-")[-1][:9]


class ValidatePersonCertificate_Request_Serializer(serializers.ModelSerializer):

    def __init__(self, *args, **kwargs):
        self.time_messages = {}
        self.log_sector = 'validate_cert'
        return super().__init__(*args, **kwargs)
    
    def get_institution(self):
        return Institution.objects.filter(administrative_institution=True).first()

    def call_BCCR(self, data):
        """
        Hace la petición de validación en el servicio del BCCR

        :return: Nada
        """
        institution = self.get_institution()
        client = ClienteValidador(negocio=institution.bccr_bussiness, entidad=institution.bccr_entity)
        self.time_messages['start_bccr_call'] = timezone.now()
        if client.validar_servicio('certificado'):
            bccrdata = client.validar_certificado_autenticacion(data['document'])
            bccrdata['code'] = get_code_from_uuid(str(uuid.uuid4()))
        else:
            logger.warning({'message': "Validate certificate BCCR not available", 'location': __file__},
                           sector=self.log_sector)
            bccrdata = client.DEFAULT_CERTIFICATE_ERROR
            bccrdata['code'] = 'N/D'
        self.time_messages['end_bccr_call'] = timezone.now()
        logger.debug({'message': "Validator BCCR: certificate ", 'data': data, 'location': __file__},
                     sector=self.log_sector)

        data['status'] = bccrdata['codigo_error']
        data['code'] = bccrdata['code']
        if 'texto_codigo_error' in bccrdata:
            data['status_text'] = bccrdata['texto_codigo_error']
        else:
            data['status_text'] = get_text_representation(ERRORES_VALIDA_CERTIFICADO, bccrdata['codigo_error'])
        data['was_successfully'] = bccrdata['exitosa']

        if bccrdata['exitosa']:
            data['identification'] = bccrdata['certificado']['identificacion']
            data['full_name'] = bccrdata['certificado']['nombre']
            data['start_validity'] = bccrdata['certificado']['inicio_vigencia']
            data['end_validity'] = bccrdata['certificado']['fin_vigencia']

        else:
            data['identification'] = None
            data['full_name'] = None
            data['start_validity'] = None
            data['end_validity'] = None
        self.time_messages['transaction_status'] = data['status']
        self.time_messages['transaction_status_text'] = data['status_text']
        self.time_messages['transaction_success'] = data['was_successfully']
        return data

    def create(self, validated_data):
        validated_data = self.call_BCCR(validated_data)
        self.time_messages['start_save_database'] = timezone.now()
        self.instance = super().create(validated_data=validated_data)
        self.time_messages['end_save_database'] = timezone.now()
        self._data = {key:validated_data[key] for key in RESPONSE_CERTIFICATE_FIELDS}
        return self.instance


    class Meta:
        model = ValidatePersonCertificateRequest
        fields = ('person', 'document', 'request_datetime', 'format')


class WarningsSerializer(serializers.ModelSerializer):
    class Meta:
        model = WarningReceived
        fields = ['description']


class ErrorFoundSerializer(serializers.ModelSerializer):
    class Meta:
        model = ErrorFound
        fields = ['code', 'detail']


class SignerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Signer
        fields = ('identification_number', 'signature_date', 'full_name')


class DocumentSeralizer(serializers.ModelSerializer):
    warnings = WarningsSerializer(many=True)
    errors = ErrorFoundSerializer(many=True)
    signers = SignerSerializer(many=True)

    class Meta:
        model = ValidatePersonDocumentRequest
        fields = ['warnings', 'errors', 'signers', 'request_datetime', 'format', 'status', 'status_text',
                  'was_successfully', 'arrived_time'
]


class ValidatePersonDocument_Request_Serializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        self.time_messages = {}
        self.log_sector = 'sign'
        return super().__init__(*args, **kwargs)

    def get_institution(self):
        return Institution.objects.filter(administrative_institution=True).first()


    def get_default_error(self, data):
        """
        Retorna la estructura de datos de error adecuada dependiendo del formato del documento

        :return: dict - Respuesta de error según formato
        """
        dev = ERRORES_VALIDAR_XMLCOFIRMA
        if data['format'] == 'cofirma':
            dev = ERRORES_VALIDAR_XMLCOFIRMA
        elif data['format'] == 'contrafirma':
            dev = ERRORES_VALIDAR_XMLCONTRAFIRMA
        elif data['format'] == 'msoffice':
            dev = ERRORES_VALIDAR_MSOFFICE
        elif data['format'] == 'odf':
            dev = ERRORES_VALIDAR_ODF
        elif data['format'] == 'pdf':
            dev = ERRORES_VALIDAR_PDF
        return dev

    def call_BCCR(self, data):
        """
        Llama al Validador de documentos del BCCR

        :return:  Nada
        """
        
        institution = self.get_institution()
        client = ClienteValidador(negocio=institution.bccr_bussiness, entidad=institution.bccr_entity)
        self.time_messages['start_bccr_call'] = timezone.now()
        if client.validar_servicio('documento'):
            bccrdata = client.validar_documento(data['document'], data['format'])

        else:
            logger.warning({'message': "Validate document BCCR not available", 'location': __file__},
                           sector=self.log_sector)
            bccrdata = client.DEFAULT_DOCUMENT_ERROR(self.get_default_error(data))
        self.time_messages['end_bccr_call'] = timezone.now()
        logger.debug({'message': "Validator BCCR:  document", 'data': bccrdata, 'location': __file__},
                     sector=self.log_sector)

        data['status'] = bccrdata['codigo_error']
        if 'texto_codigo_error' in data:
            data['status_text'] = bccrdata['texto_codigo_error']
        else:
            data['status_text'] = get_text_representation(self.get_default_error(data),  bccrdata['codigo_error'])
        data['was_successfully'] = bccrdata['exitosa']
        data['response_datetime'] = timezone.now()

        self.time_messages['transaction_status'] = data['status']
        self.time_messages['transaction_status_text'] = data['status_text'] 
        self.time_messages['transaction_success'] = settings.DEFAULT_SUCCESS_BCCR == data['status']

        return data, bccrdata

    def get_signers(self, signers):
        """
        Extrae la información de los firmantes del documento

        :param signers:  Lista de firmantes del documento recibido del BCCR
        :return: Nada
        """
        if signers is None:
            return
        for signer in signers:
            signerobj = Signer.objects.create(
                identification_number=signer['identificacion'],
                signature_date=signer['fecha_firma'],
                full_name=signer['nombre']
            )
            self.instance.signers.add(signerobj)

    def get_found_errors(self, errors):
        """
        Retorna la lista de errores encontrados en el documento

        :param errors: Lista datos de error del BCCR
        :return: Nada
        """
        if errors is None:
            return
        for error in errors:
            error, _ = ErrorFound.objects.get_or_create(
                code=error[0],
                detail=error[1]
            )
            self.instance.errors.add(error)

    def get_warnings(self, warnings):
        """
        Extrae las advertencias del documento de la información obtenida del BCCR

        :param warnings: Lista de advertencias del BCCR
        :return: Nada
        """
        if warnings is None:
            return
        for warning in warnings:
            if warning:
                adv, _ = WarningReceived.objects.get_or_create(
                    description=warning
                )
                self.instance.warnings.add(adv)

    def create(self, validated_data):
        validated_data, bccrdata = self.call_BCCR(validated_data)
        self.time_messages['start_save_database'] = timezone.now()
        self.instance = super().create(validated_data=validated_data)
        self.get_warnings(bccrdata['advertencias'])
        self.get_found_errors(bccrdata['errores_encontrados'])
        self.get_signers(bccrdata['firmantes'])
        self.time_messages['end_save_database'] = timezone.now()
        response_serializer = DocumentSeralizer(self.instance)
        self._data = response_serializer.data
        return self.instance

    class Meta:
        model = ValidatePersonDocumentRequest
        fields = ('person', 'document', 'request_datetime', 'format')


class ValidatePersonCertificateRequest_Response_Serializer(
        serializers.ModelSerializer):
    class Meta:
        model = ValidatePersonCertificateRequest
        fields = ('identification', 'request_datetime',
                  'code', 'status', 'status_text',
                  'full_name', 'start_validity', 'end_validity',
                  'was_successfully')


class ValidatePersonDocumentRequest_Response_Serializer(
        ValidateDocument_ResponseSerializer):
    class Meta:
        model = ValidatePersonDocumentRequest
        fields = ('request_datetime', 'format',
                  'code', 'status', 'status_text',
                  'warnings', 'errors', 'signers',
                  'was_successfully')


class SuscriptorPerson_Serializer(serializers.Serializer):
    def __init__(self, *args, **kwargs):
        self.time_messages = {}
        self.log_sector = 'sign'
        return super().__init__(*args, **kwargs)

    def get_institution(self):
        return Institution.objects.filter(administrative_institution=True).first()


    def call_BCCR(self, requestdata):
        """
        Llama al métido de verificar si el suscriptor está conectado.

        .. note:: Si existe algún problema de comunicación con el BCCR se responde como False, aunque el usuario si esté
                  conectado, pero ante la imposibilidad de determinar si lo está o no, se prefiere el no está conectado

        :return: True o False dependiendo el suscriptor está desconectado o no
        """
        institution = self.get_institution()
        signclient = ClienteFirmador(negocio=institution.bccr_bussiness, entidad=institution.bccr_entity)
        if signclient.validar_servicio():
            data = signclient.suscriptor_conectado(requestdata['identification'])
        else:
            logger.warning({'message': "Sign/Validate:  BCCR No disponible", 'location': __file__},
                           sector=self.log_sector)
            data = False
        logger.debug({'message': 'Subscriptor ', 'data': data, 'location': __file__}, sector=self.log_sector)
        return data

