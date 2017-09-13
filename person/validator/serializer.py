'''
Created on 13 sep. 2017

@author: luisza
'''
from person.models import ValidatePersonDocumentDataRequest,\
    ValidatePersonCertificateDataRequest, ValidatePersonDocumentRequest,\
    ValidatePersonCertificateRequest
from institution.validator.serializer import ValidateDocument_ResponseSerializer
from rest_framework import serializers
from corebase.validator import ValidateDocument_RequestSerializer,\
    ValidateCertificate_RequestSerializer, Suscriptor_Serializer
from person.serializer import PersonBaseSerializer

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
        
class SuscriptorPerson_Serializer(Suscriptor_Serializer, PersonBaseSerializer):
    check_internal_fields = ['person',
                             'identification',
                             'request_datetime']

    class Meta:
        model = ValidatePersonDocumentRequest
        fields = ('person', 'data_hash', 'algorithm',
                  'public_certificate', 'data')

