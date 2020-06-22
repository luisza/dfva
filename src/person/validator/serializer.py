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


from person.models import ValidatePersonDocumentDataRequest,\
    ValidatePersonCertificateDataRequest, ValidatePersonDocumentRequest,\
    ValidatePersonCertificateRequest
from institution.validator.serializer import \
    ValidateDocument_ResponseSerializer
from rest_framework import serializers
from corebase.validator import ValidateDocument_RequestSerializer,\
    ValidateCertificate_RequestSerializer, Suscriptor_Serializer
from person.serializer import PersonBaseSerializer
from person.validator.forms import ValidateCertificateForm, ValidateDocumentForm


class ValidatePersonCertificate_Request_Serializer(
        PersonBaseSerializer,
        ValidateCertificate_RequestSerializer):
    check_internal_fields = ['person',
                             'document',
                             'request_datetime']

    validate_request_class = ValidatePersonCertificateRequest
    validate_data_class = ValidatePersonCertificateDataRequest
    form = ValidateCertificateForm
    def save_subject(self):
        self.adr.person = self.person

    class Meta:
        model = ValidatePersonCertificateRequest
        fields = ('person', 'data_hash', 'algorithm',
                  'public_certificate', 'data')


class ValidatePersonDocument_Request_Serializer(
        PersonBaseSerializer,
        ValidateDocument_RequestSerializer):
    check_internal_fields = ['person',
                             'document',
                             'format',
                             'request_datetime']

    validate_request_class = ValidatePersonDocumentRequest
    validate_data_class = ValidatePersonDocumentDataRequest
    form = ValidateDocumentForm

    def save_subject(self):
        self.adr.person = self.person

    class Meta:
        model = ValidatePersonDocumentRequest
        fields = ('person', 'data_hash', 'algorithm',
                  'public_certificate', 'data')


class ValidatePersonCertificateRequest_Response_Serializer(
        serializers.ModelSerializer):
    class Meta:
        model = ValidatePersonCertificateDataRequest
        fields = ('identification', 'request_datetime',
                  'code', 'status', 'status_text',
                  'full_name', 'start_validity', 'end_validity',
                  'was_successfully')


class ValidatePersonDocumentRequest_Response_Serializer(
        ValidateDocument_ResponseSerializer):
    class Meta:
        model = ValidatePersonDocumentDataRequest
        fields = ('request_datetime', 'format',
                  'code', 'status', 'status_text',
                  'warnings', 'errors', 'signers',
                  'was_successfully')


class SuscriptorPerson_Serializer(Suscriptor_Serializer, PersonBaseSerializer):
    check_internal_fields = ['person',
                             'identification',
                             'request_datetime']

    class Meta:
        model = ValidatePersonDocumentRequest
        fields = ('person', 'data_hash', 'algorithm',
                  'public_certificate', 'data')
