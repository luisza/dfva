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

from institution.authenticator.forms import AuthenticateForm, AuthenticateCheckForm
from institution.models import AuthenticateRequest, AuthenticateDataRequest
from corebase.authenticate import Authenticate_RequestSerializer
from rest_framework import serializers
from institution.serializer import InstitutionCheckBaseBaseSerializer
from django.conf import settings

logger = logging.getLogger(settings.DEFAULT_LOGGER_NAME)


class Authenticate_Request_Serializer(InstitutionCheckBaseBaseSerializer,
                                      Authenticate_RequestSerializer):

    check_internal_fields = ['notification_url', 'identification',
                             'request_datetime', 'institution']

    check_show_fields = ['institution',
                         'notification_url',
                         # 'identification',
                         'request_datetime']

    form = AuthenticateForm
    form_check = AuthenticateCheckForm

    validate_request_class = AuthenticateRequest
    validate_data_class = AuthenticateDataRequest

    def save_subject(self):
        self.adr.notification_url = self.requestdata['notification_url']
        self.adr.identification = self.requestdata['identification']

    class Meta:
        model = AuthenticateRequest
        fields = ('institution', 'data_hash', 'algorithm',
                  'public_certificate', 'data', 'encrypt_method')


class Authenticate_Response_Serializer(serializers.ModelSerializer):

    class Meta:
        model = AuthenticateDataRequest
        fields = (
            'code', 'status', 'identification', 'id_transaction',
            'request_datetime', 'sign_document', 'expiration_datetime',
            'received_notification', 'duration', 'status_text', 'resume',
            'hash_docsigned',  'hash_id_docsigned'
        )


class LogAuthenticateInstitutionRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthenticateDataRequest
        fields = ('institution', 'notification_url', 'identification',
                  'request_datetime', 'code', 'status', 'status_text',
                  'response_datetime', 'expiration_datetime', 'id_transaction',
                  'duration', 'received_notification', 'resume'
                  )
