import logging

from corebase.signer import Sign_RequestSerializer
from corebase.models import SUPPORTED_DOC_FORMAT
from person.models import SignPersonRequest, SignPersonDataRequest
from person.serializer import PersonCheckBaseBaseSerializer
from rest_framework import serializers
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

logger = logging.getLogger(settings.DEFAULT_LOGGER_NAME)


class Sign_Person_Request_Serializer(PersonCheckBaseBaseSerializer,
                                     Sign_RequestSerializer):

    check_internal_fields = ['person',
                             'document',
                             'format',
                             'algorithm_hash',
                             'document_hash',
                             'resumen',
                             'identification',
                             'request_datetime']

    check_show_fields = ['person',
                         'identification',
                         'request_datetime']

    validate_request_class = SignPersonRequest
    validate_data_class = SignPersonDataRequest

    def check_internal_data(self, data, fields=[]):
        super(Sign_Person_Request_Serializer,
              self).check_internal_data(data, fields=fields)

        if 'format' in data:
            if data['format'].lower() not in SUPPORTED_DOC_FORMAT:
                self._errors['format'] = [
                    _('Format not supported, sopported formats are %s') % (
                        " ".join(SUPPORTED_DOC_FORMAT))]

    def save_subject(self):
        self.adr.person = self.person

    class Meta:
        model = SignPersonRequest
        fields = ('person', 'data_hash', 'algorithm',
                  'public_certificate', 'data')


class Sign_Person_Response_Serializer(serializers.ModelSerializer):

    class Meta:
        model = SignPersonDataRequest
        fields = (
            'code', 'status', 'identification', 'id_transaction',
            'sign_document', 'duration', 'status_text',
            'request_datetime', 'expiration_datetime', 'received_notification')
