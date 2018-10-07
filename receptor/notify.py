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
@date: 30/7/2017
@author: Luis Zarate Montero
@contact: luis.zarate@solvosoft.com
@license: GPLv3
'''

import requests
from rest_framework.renderers import JSONRenderer
from corebase.rsa import encrypt, get_hash_sum
import logging
from institution.models import AuthenticateDataRequest, SignDataRequest
from institution.authenticator.serializer import \
    Authenticate_Response_Serializer
from institution.signer.serializer import Sign_Response_Serializer
from django.conf import settings

logger = logging.getLogger(settings.DEFAULT_LOGGER_NAME)


def get_datarequest_serializer(data):
    if isinstance(data, AuthenticateDataRequest):
        return Authenticate_Response_Serializer, data.authenticaterequest
    elif isinstance(data, SignDataRequest):
        return Sign_Response_Serializer, data.signrequest


def send_notification(data, serializer=None, request=None,
                      encrypt_method='aes_eax'):
    """
    Envia notificación a la institución, cuando se recibe una respuesta por parte del BCCR, este método 
    reenvía la respuesta a la URL especificada en la petición. 

    La estructura de envío es:

    :params id_transaction: Id de transacción del BCCR
    :params data: Es un diccionario con los siguientes atributos

        * **code:**  Código de identificación de la transacción (no es el mismo que el que se muestra en al usuario en firma)
        * **identification:** Identificador del suscriptor
        * **id_transaction:** Id de trasnacción en el FVA del BCCR
        * **request_datetime:** Hora de recepción de la solicitud
        * **sign_document:** Almacena el documento, pero no se garantiza que venga el documento firmado, puede ser None
        * **expiration_datetime:** Hora de recepción de la solicitud
        * **received_notification:** True si la autenticación ha sido procesada, False si está esperando al usuario
        * **duration:**  tiempo que duró entre que fue enviada y fue recibida
        * **status:**   Código de error de la transacción
        * **status_text:**  Descripción en texto del estado

    :params hashsum: Suma hash realizada a data
    :params algorithm: Algoritmo con el que se realizó la suma hash

    Por defecto se utiliza el método de encripción seleccionado al realizar la petición por parte de la institución, pero en caso de no lograrse 
    identificar el método se utiliza por defecto 'aes_eax'

    """

    if data.notification_url == 'N/D':
        return

    if serializer is None:
        serializer, req = get_datarequest_serializer(data)

    ars = serializer(data)
    datajson = JSONRenderer().render(ars.data)
    edata = encrypt(data.institution.public_key,
                    datajson, method=encrypt_method)
    hashsum = get_hash_sum(edata, req.algorithm)
    error = None
    try:
        response = requests.post(data.notification_url,
                                 data={'id_transaction': data.id_transaction,
                                       'data': edata.decode(),
                                       'hashsum': hashsum,
                                       'algorithm': req.algorithm})
        response.raise_for_status()
    except Exception as e:
        error = e
        logger.error('Receptor: notificando a %s lanza %s' %
                     (data.notification_url, e))

    return error
