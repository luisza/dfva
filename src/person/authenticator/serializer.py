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

from institution.authenticator.forms import AuthenticateCheckForm
from person.authenticator.forms import AuthenticatePersonForm
from person.models import AuthenticatePersonRequest,\
    AuthenticatePersonDataRequest
from rest_framework import serializers
import logging
from corebase.authenticate import Authenticate_RequestSerializer
from person.serializer import PersonCheckBaseBaseSerializer
from django.conf import settings


logger = logging.getLogger(settings.DEFAULT_LOGGER_NAME)


class Authenticate_Person_Request_Serializer(PersonCheckBaseBaseSerializer,
                                             Authenticate_RequestSerializer):

    check_internal_fields = ['identification',
                             'request_datetime', 'person']
    check_show_fields = ['person',
                         'identification',
                         'request_datetime']

    form = AuthenticatePersonForm
    form_check = AuthenticateCheckForm
    validate_request_class = AuthenticatePersonRequest
    validate_data_class = AuthenticatePersonDataRequest

    def save_subject(self):
        self.adr.person = self.person
        self.adr.identification = self.requestdata['identification']

    class Meta:
        model = AuthenticatePersonRequest
        fields = ('person', 'data_hash', 'algorithm',
                  'public_certificate', 'data')


class Authenticate_Person_Response_Serializer(serializers.ModelSerializer):

    class Meta:
        model = AuthenticatePersonDataRequest
        fields = (
            'code', 'status', 'identification', 'id_transaction',
            'request_datetime', 'sign_document', 'expiration_datetime',
            'received_notification', 'duration', 'status_text')
