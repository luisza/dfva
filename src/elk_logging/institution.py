
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