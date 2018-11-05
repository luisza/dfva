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

import logging
from django.utils import timezone
from corebase.time import parse_datetime
from rest_framework import serializers
from pyfva.clientes.firmador import ClienteFirmador
from django.conf import settings

logger = logging.getLogger(settings.DEFAULT_LOGGER_NAME)


class Sign_RequestSerializer(serializers.HyperlinkedModelSerializer):

    data = serializers.CharField(
        help_text="""Datos de solicitud de autenticación encriptados usando 
        AES.MODE_EAX con la llave de sesión encriptada con PKCS1_OAEP
         """)
    readonly_fields = ['data']

    def call_BCCR(self):
        signclient = ClienteFirmador(
            negocio=self.institution.bccr_bussiness,
            entidad=self.institution.bccr_entity,
        )
        if signclient.validar_servicio():
            data = signclient.firme(
                self.requestdata['identification'],
                self.requestdata['document'],
                self.requestdata['format'],
                algoritmo_hash=self.requestdata['algorithm_hash'].title(),
                hash_doc=self.requestdata['document_hash'],
                resumen=self.requestdata['resumen'],
                lugar=self.requestdata['place'] if 'place' in self.requestdata else None,
                razon=self.requestdata['reason'] if 'reason' in self.requestdata else None
            )
        else:
            logger.warning("Sign BCCR not available")
            data = signclient.DEFAULT_ERROR

        logger.debug("Sign BCCR: %r" % (data, ))
        self.save_subject()
        self.adr.identification = self.requestdata['identification']
        self.adr.request_datetime = parse_datetime(
            self.requestdata['request_datetime'])
        self.adr.duration = data['tiempo_maximo']
        if 'texto_codigo_error' in data:
            self.adr.status_text = data['texto_codigo_error']
        self.adr.expiration_datetime = timezone.now(
        ) + timezone.timedelta(minutes=data['tiempo_maximo'])

        self.adr.status = data['codigo_error']
        self.adr.id_transaction = data['id_solicitud']
        self.adr.code = data['codigo_verificacion'] or 'N/D'
        self.adr.document_format = self.requestdata['format']

        self.adr.lugar = self.requestdata['place'] if 'place' in self.requestdata else None
        self.adr.razon = self.requestdata['reason'] if 'reason' in self.requestdata else None

    def save(self, **kwargs):
        odata = {}
        for field in self.Meta.fields:
            if field == 'data':
                continue
            if field in self.data:
                odata[field] = self.data[field]

        auth_request = self.validate_request_class(**odata)
        self.adr = self.validate_data_class()
        self.call_BCCR()
        self.adr.save()

        auth_request.data_request = self.adr
        auth_request.save()
        return auth_request
