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
@date: 14/4/2017
@author: Luis Zarate Montero
@contact: luis.zarate@solvosoft.com
@license: GPLv3
'''

import logging

from django.utils import timezone

from corebase.signer import Sign_RequestSerializer
from corebase.models import SUPPORTED_DOC_FORMAT
from institution.models import Institution
from person.models import SignPersonRequest
from person.serializer import PersonCheckBaseBaseSerializer
from rest_framework import serializers
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from pyfva.clientes.firmador import ClienteFirmador
from corebase.time import parse_datetime

logger = logging.getLogger(settings.DEFAULT_LOGGER_NAME)
RESPONSE_FIELDS = ('code', 'status', 'identification', 'id_transaction', 'signed_document', 'duration', 'status_text',
                  'request_datetime', 'expiration_datetime', 'received_notification', 'hash_docsigned',
                  'hash_id_docsigned')


class Sign_Person_Request_Serializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        self.time_messages = {}
        self.log_sector = 'sign'
        return super().__init__(*args, **kwargs)

    def get_institution(self):
        return Institution.objects.filter(administrative_institution=True).first()

    def call_BCCR(self, data):
        """
        Llama la función de firma de documentos del BCCR.

        :return: Nada
        """
        institution = self.get_institution()
        signclient = ClienteFirmador(
            negocio=institution.bccr_bussiness,
            entidad=institution.bccr_entity,
        )
        self.time_messages['start_bccr_call'] = timezone.now()
        if signclient.validar_servicio():
            bccrdata = signclient.firme(
                data['identification'],
                data['document'],
                data['format'],
                algoritmo_hash=data['algorithm_hash'].title(),
                hash_doc=data['document_hash'],
                resumen=data['resume'],
                lugar=data['place'] if 'place' in data else None,
                razon=data['reason'] if 'reason' in data else None
            )
        else:
            logger.warning({'message': "Sign BCCR not available", 'location': __file__}, sector=self.log_sector)
            data = signclient.DEFAULT_ERROR
        self.time_messages['end_bccr_call'] = timezone.now()
        logger.debug({'message': "Sign BCCR", 'data': data, 'location': __file__}, sector=self.log_sector)

        data['duration'] = bccrdata['tiempo_maximo']
        data['status_text'] = bccrdata['texto_codigo_error']
        data['expiration_datetime'] = timezone.now() + timezone.timedelta(minutes=bccrdata['tiempo_maximo'])
        data['status'] = bccrdata['codigo_error']
        data['id_transaction'] = bccrdata['id_solicitud']
        data['code'] = bccrdata['codigo_verificacion'] or 'N/D'

        self.time_messages['transaction_status'] = data['status']
        self.time_messages['transaction_status_text'] = data['status_text']
        self.time_messages['transaction_success'] = settings.DEFAULT_SUCCESS_BCCR == data['status']
        return data

    def create(self, validated_data):
        validated_data = self.call_BCCR(validated_data)
        self.time_messages['start_save_database'] = timezone.now()
        instance = super().create(validated_data=validated_data)
        self.time_messages['end_save_database'] = timezone.now()
        validated_data['signed_document'] = None
        validated_data['received_notification'] = False
        validated_data['hash_docsigned'] = None
        validated_data['hash_id_docsigned'] = None
        self._data = {key: validated_data[key] for key in RESPONSE_FIELDS}
        self._data['id'] = instance.pk
        return instance

    class Meta:
        model = SignPersonRequest
        fields = ('person', 'identification', 'request_datetime', 'document', 'format', 'place',
                    'reason', 'algorithm_hash', 'document_hash', 'resume', 'public_certificate')


class Sign_Person_Response_Serializer(serializers.ModelSerializer):
    class Meta:
        model = SignPersonRequest
        fields = RESPONSE_FIELDS
