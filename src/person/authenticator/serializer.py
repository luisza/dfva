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
from django.utils import timezone

from institution.models import Institution
from person.models import AuthenticatePersonRequest
from rest_framework import serializers
import logging
from pyfva.clientes.autenticador import ClienteAutenticador
from pyfva.constants import get_text_representation, ERRORES_AL_SOLICITAR_FIRMA
from django.conf import settings
from corebase.time import parse_datetime

logger = logging.getLogger(settings.DEFAULT_LOGGER_NAME)
RESPONSE_FIELDS = ('code', 'status', 'identification', 'id_transaction', 'request_datetime', 'signed_document',
                   'expiration_datetime', 'received_notification', 'duration', 'status_text')


class Authenticate_Person_Request_Serializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        self.time_messages = {}
        self.log_sector = 'sign'
        return super().__init__(*args, **kwargs)

    def get_institution(self):
        return Institution.objects.filter(administrative_institution=True).first()

    def call_BCCR(self, requestdata):
        """
        Llama a la funcion de autenticación del BCCR

        """
        institution = self.get_institution()
        authclient = ClienteAutenticador(institution.bccr_bussiness, institution.bccr_entity)
        self.time_messages['start_bccr_call'] = timezone.now()
        if authclient.validar_servicio():
            data = authclient.solicitar_autenticacion(requestdata['identification'])
        else:
            logger.warning({'message':"Auth BCCR not available", 'location': __file__})
            data = authclient.DEFAULT_ERROR
        self.time_messages['end_bccr_call'] = timezone.now()
        logger.debug({'message': "Authentication BCCR", 'data': data,  'location': __file__})
        requestdata['expiration_datetime'] = timezone.now() + timezone.timedelta(minutes=data['tiempo_maximo'])
        requestdata['duration'] = data['tiempo_maximo']
        if 'texto_codigo_error' in data:
            requestdata['status_text'] = data['texto_codigo_error']
        else:
            requestdata['status_text'] = get_text_representation(ERRORES_AL_SOLICITAR_FIRMA,  data['codigo_error'])
        requestdata['status'] = data['codigo_error']
        requestdata['id_transaction'] = data['id_solicitud']
        requestdata['code'] = data['codigo_verificacion'] or 'N/D'
        requestdata['resume'] = data['resumen'] if 'resumen' in data else None
        requestdata['signed_document'] = None
        requestdata['received_notification'] = False
        self.time_messages['transaction_status'] = requestdata['status']
        self.time_messages['transaction_status_text'] = requestdata['status_text']
        self.time_messages['transaction_success'] = settings.DEFAULT_SUCCESS_BCCR == requestdata['status']
        return requestdata

    def create(self, validated_data):
        validated_data = self.call_BCCR(validated_data)
        self.time_messages['start_save_database'] = timezone.now()
        instance = super().create(validated_data=validated_data)
        self.time_messages['end_save_database'] = timezone.now()
        self._data = {key: validated_data[key] for key in RESPONSE_FIELDS}
        self._data['id'] = instance.pk
        return instance

    class Meta:
        model = AuthenticatePersonRequest
        fields = ('person', 'identification', 'request_datetime', 'public_certificate')


class Authenticate_Person_Response_Serializer(serializers.ModelSerializer):
    class Meta:
        model = AuthenticatePersonRequest
        fields = RESPONSE_FIELDS


class LogAuthenticateInstitutionRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthenticatePersonRequest
        fields = '__all__'