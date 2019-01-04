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
@date: 1/01/2019
@author: Universidad de Costa Rica
@maintainer: Luis Zarate Montero
@contact: luis.zarate@solvosoft.com
@license: GPLv3
'''



from institution.models import AuthenticateDataRequest, SignDataRequest, ValidateCertificateDataRequest, \
    ValidateDocumentDataRequest
from django_elasticsearch_dsl import DocType, Index, TextField

authInstitution = Index('authenticate_institution')
authInstitution.settings(
    number_of_shards=1,
    number_of_replicas=0
)


@authInstitution.doc_type
class AuthenticateInstitutionDocument(DocType):
    institution = TextField()
    institution_name = TextField()

    def prepare_institution(self, instance):
        return str(instance.institution.code)

    def prepare_institution_name(self, instance):
        return str(instance.institution)

    class Meta:
        model = AuthenticateDataRequest
        fields = ['id', 'request_datetime', 'identification', 'status', 'status_text', 'response_datetime',
                  'received_notification', 'id_transaction', 'arrived_time', 'update_time']




signInstitution = Index('sign_institution')
signInstitution.settings(
    number_of_shards=1,
    number_of_replicas=0
)

@signInstitution.doc_type
class SignInstitutionDocument(DocType):
    institution = TextField()
    institution_name = TextField()

    def prepare_institution(self, instance):
        return str(instance.institution.code)

    def prepare_institution_name(self, instance):
        return str(instance.institution)

    class Meta:
        model = SignDataRequest
        fields = ['id', 'request_datetime', 'identification', 'status', 'status_text', 'response_datetime',
                  'received_notification', 'id_transaction', 'arrived_time', 'update_time',
                  'document_format', 'place', 'reason']


validateCertificateInstitution = Index('validatecertificate_institution')
validateCertificateInstitution.settings(
    number_of_shards=1,
    number_of_replicas=0
)

@validateCertificateInstitution.doc_type
class validateCertificateDocument(DocType):
    institution = TextField()
    institution_name = TextField()

    def prepare_institution(self, instance):
        return str(instance.institution.code)

    def prepare_institution_name(self, instance):
        return str(instance.institution)

    class Meta:
        model = ValidateCertificateDataRequest
        fields = ['id', 'request_datetime', 'identification', 'status', 'status_text', 'response_datetime',
                   'arrived_time', 'update_time', 'was_successfully', 'full_name', 'start_validity', 'end_validity']



validateDocumentInstitution = Index('validatedocument_institution')
validateDocumentInstitution.settings(
    number_of_shards=1,
    number_of_replicas=0
)

@validateDocumentInstitution.doc_type
class validateDocumentInstitutionDocument(DocType):
    institution = TextField()
    institution_name = TextField()
    status_text = TextField()

    def prepare_institution(self, instance):
        return str(instance.institution.code)

    def prepare_institution_name(self, instance):
        return str(instance.institution)

    def prepare_status_text(self, instance):
        return instance.get_status_display()

    class Meta:
        model = ValidateDocumentDataRequest
        fields = ['id', 'arrived_time', 'update_time', 'was_successfully', 'status',
                   'format', 'request_datetime']