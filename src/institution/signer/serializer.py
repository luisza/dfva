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
@author: Universidad de Costa Rica
@maintainer: Luis Zarate Montero
@contact: luis.zarate@solvosoft.com
@license: GPLv3
'''

import logging
from corebase.signer import Sign_RequestSerializer
from institution.models import SignRequest, SignDataRequest
from rest_framework import serializers
from institution.serializer import InstitutionCheckBaseBaseSerializer
from django.conf import settings

from institution.signer.forms import SignDataForm, SignDataCheckForm

logger = logging.getLogger(settings.DEFAULT_LOGGER_NAME)


class Sign_Request_Serializer(InstitutionCheckBaseBaseSerializer,
                              Sign_RequestSerializer):

    check_internal_fields = ['institution',
                             'notification_url',
                             'document',
                             'format',
                             'algorithm_hash',
                             'document_hash',
                             'resumen',
                             'identification',
                             'request_datetime']
    check_show_fields = ['institution',
                         'notification_url',
                         # 'identification',
                         'request_datetime']

    validate_request_class = SignRequest
    validate_data_class = SignDataRequest

    form = SignDataForm
    form_check = SignDataCheckForm

    def check_received_extra_data(self, data):
        if 'format' not in data:
            return

        if data['format'] == 'pdf':
            for field in ['reason', 'place']:
                if field not in data or data[field] is None:
                    self._errors[field] = ['%s not found' % (field)]

    def save_subject(self):
        self.adr.notification_url = self.requestdata['notification_url']
        self.adr.institution = self.institution

    class Meta:
        model = SignRequest
        fields = ('institution', 'data_hash', 'algorithm',
                  'public_certificate', 'data', 'encrypt_method')


class Sign_Response_Serializer(serializers.ModelSerializer):
    class Meta:
        model = SignDataRequest
        fields = (
            'code', 'status', 'identification', 'id_transaction',
            'sign_document', 'duration', 'status_text',
            'request_datetime', 'expiration_datetime',
            'received_notification', 'resume', 'hash_docsigned',
            'hash_id_docsigned'
        )


class LogSingInstitutionRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = SignDataRequest
        fields = (
            'institution', 'notification_url', 'identification',
            'request_datetime', 'code', 'status', 'status_text',
            'response_datetime', 'expiration_datetime', 'id_transaction',
            'duration', 'received_notification', 'resume'
        )
