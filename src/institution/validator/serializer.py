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
@date: 13/9/2017
@author: Universidad de Costa Rica
@maintainer: Luis Zarate Montero
@contact: luis.zarate@solvosoft.com
@license: GPLv3
'''

from corebase.validator import ValidateCertificate_RequestSerializer,\
    ValidateDocument_RequestSerializer, Suscriptor_Serializer
from institution.models import ValidateCertificateRequest,\
    ValidateCertificateDataRequest, ValidateDocumentDataRequest,\
    ValidateDocumentRequest
from rest_framework import serializers
from corebase.validator import SignerSerializer, ErrorFoundSerializer
from institution.serializer import InstitutionBaseSerializer


class ValidateCertificate_Request_Serializer(
        InstitutionBaseSerializer,
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


class ValidateCertificateRequest_Response_Serializer(
        serializers.ModelSerializer):
    class Meta:
        model = ValidateCertificateDataRequest
        fields = ('identification', 'request_datetime',
                  'code', 'status', 'id_transaction',
                  'status_text', 'full_name',
                  'start_validity', 'end_validity',
                  'was_successfully')


class ValidateDocument_ResponseSerializer(serializers.ModelSerializer):
    warnings = serializers.StringRelatedField(many=True)
    signers = SignerSerializer(many=True)
    errors = ErrorFoundSerializer(many=True)


class ValidateDocumentRequest_Response_Serializer(
        ValidateDocument_ResponseSerializer):
    class Meta:
        model = ValidateDocumentDataRequest
        fields = ('request_datetime',
                  'code', 'status', 'status_text',
                  'warnings', 'errors', 'signers',
                  'was_successfully')


class ValidateDocument_Request_Serializer(InstitutionBaseSerializer,
                                          ValidateDocument_RequestSerializer):
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


class SuscriptorInstitution_Serializer(Suscriptor_Serializer,
                                       InstitutionBaseSerializer):
    check_internal_fields = ['institution',
                             'notification_url',
                             'identification',
                             'request_datetime']

    class Meta:
        model = ValidateDocumentRequest
        fields = ('institution', 'data_hash', 'algorithm',
                  'public_certificate', 'data', 'encrypt_method')
