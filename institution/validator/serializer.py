'''
Created on 13 sep. 2017

@author: luisza
'''

from corebase.validator import ValidateCertificate_RequestSerializer,\
    ValidateDocument_RequestSerializer, Suscriptor_Serializer
from institution.models import ValidateCertificateRequest,\
    ValidateCertificateDataRequest, ValidateDocumentDataRequest,\
    ValidateDocumentRequest
from rest_framework import serializers
from corebase.validator import FirmanteSerializer, ErrorEncontradoSerializer
from institution.serializer import InstitutionBaseSerializer

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
                  'public_certificate', 'data', 'encrypt_method')


class ValidateCertificateRequest_Response_Serializer(serializers.ModelSerializer):
    class Meta:
        model = ValidateCertificateDataRequest
        fields = ('identification', 'request_datetime',
                  'code', 'status', 'id_transaction',
                  'status_text', 'nombre_completo', 'inicio_vigencia', 'fin_vigencia',
                  'fue_exitosa')

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
                             'document', 'format',
                             'request_datetime']

    validate_request_class = ValidateDocumentRequest
    validate_data_class = ValidateDocumentDataRequest

    def save_subject(self):
        self.adr.notification_url = self.requestdata['notification_url']
        self.adr.institution = self.institution

    class Meta:
        model = ValidateDocumentRequest
        fields = ('institution', 'data_hash', 'algorithm',
                  'public_certificate', 'data', 'encrypt_method')

class SuscriptorInstitution_Serializer(Suscriptor_Serializer, InstitutionBaseSerializer):
    check_internal_fields = ['institution',
                             'notification_url',
                             'identification',
                             'request_datetime']

    class Meta:
        model = ValidateDocumentRequest
        fields = ('institution', 'data_hash', 'algorithm',
                  'public_certificate', 'data', 'encrypt_method')
