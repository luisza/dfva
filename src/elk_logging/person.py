from django_elasticsearch_dsl import DocType, Index, TextField

from person.models import AuthenticatePersonDataRequest, SignPersonDataRequest, ValidatePersonCertificateDataRequest, \
    ValidatePersonDocumentDataRequest

authPerson = Index('authenticate_person')
authPerson.settings(
    number_of_shards=1,
    number_of_replicas=0
)


@authPerson.doc_type
class AuthenticatePersonDocument(DocType):
    person_identification = TextField()
    person_name = TextField()

    def prepare_person_identification(self, instance):
        return instance.person.identification

    def prepare_person_name(self, instance):
        return instance.person.get_full_name()

    class Meta:
        model = AuthenticatePersonDataRequest
        fields = ['id', 'request_datetime', 'identification', 'status', 'status_text', 'response_datetime',
                  'received_notification', 'id_transaction', 'arrived_time', 'update_time']


signPerson = Index('sign_person')
signPerson.settings(
    number_of_shards=1,
    number_of_replicas=0
)


@signPerson.doc_type
class SignPersonDocument(DocType):
    person_identification = TextField()
    person_name = TextField()

    def prepare_person_identification(self, instance):
        return instance.person.identification

    def prepare_person_name(self, instance):
        return instance.person.get_full_name()


    class Meta:
        model = SignPersonDataRequest
        fields = ['id', 'request_datetime', 'identification', 'status', 'status_text', 'response_datetime',
                  'received_notification', 'id_transaction', 'arrived_time', 'update_time',
                  'document_format', 'place', 'reason']


validateCertificatePerson = Index('validatecertificate_person')
validateCertificatePerson.settings(
    number_of_shards=1,
    number_of_replicas=0
)


@validateCertificatePerson.doc_type
class validateCertificatePersonDocument(DocType):
    person_identification = TextField()
    person_name = TextField()

    def prepare_person_identification(self, instance):
        return instance.person.identification

    def prepare_person_name(self, instance):
        return instance.person.get_full_name()

    class Meta:
        model = ValidatePersonCertificateDataRequest
        fields = ['id', 'request_datetime', 'identification', 'status', 'status_text', 'response_datetime',
                   'arrived_time', 'update_time', 'was_successfully', 'full_name', 'start_validity', 'end_validity']


validateDocumentPerson = Index('validatedocument_person')
validateDocumentPerson.settings(
    number_of_shards=1,
    number_of_replicas=0
)

@validateDocumentPerson.doc_type
class validateDocumentPersonDocument(DocType):
    person_identification = TextField()
    person_name = TextField()
    status_text = TextField()

    def prepare_person_identification(self, instance):
        return instance.person.identification

    def prepare_person_name(self, instance):
        return instance.person.get_full_name()

    def prepare_status_text(self, instance):
        return instance.get_status_display()

    class Meta:
        model = ValidatePersonDocumentDataRequest
        fields = ['id', 'arrived_time', 'update_time', 'was_successfully', 'status',
                   'format', 'request_datetime']