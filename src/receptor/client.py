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
@date: 26/7/2017
@author: Luis Zarate Montero
@contact: luis.zarate@solvosoft.com
@license: GPLv3
'''

import binascii
import logging
from base64 import b64decode
from django.conf import settings

from pyfva.constants import ERRORES_AL_NOTIFICAR_FIRMA, \
    get_text_representation

from receptor.notify import send_notification


logger = logging.getLogger(settings.DEFAULT_LOGGER_NAME)
DATAREQUEST = []

try:
    from institution.models import AuthenticateDataRequest, SignDataRequest
    DATAREQUEST += [AuthenticateDataRequest, SignDataRequest]
except:
    pass

try:
    from person.models import AuthenticatePersonDataRequest,\
        SignPersonDataRequest
    DATAREQUEST += [AuthenticatePersonDataRequest, SignPersonDataRequest]
except:
    pass


def get_encrypt_method(datarequest):
    encrypt_method = 'aes_eax'
    if isinstance(datarequest, AuthenticateDataRequest):
        encrypt_method = datarequest.authenticaterequest.encrypt_method
    elif isinstance(datarequest, SignDataRequest):
        encrypt_method = datarequest.signrequest.encrypt_method
    return encrypt_method


def get_hashsum_b64(data):
    if data is not None:
        return binascii.hexlify(b64decode(data)).decode()


def get_document(document):
    if type(document) == str:
        return document
    return None


def reciba_notificacion(data):
    """
    Recibe la notificación del BCCR

    :params data: Es un diccionario con los siguientes atributos

        * **id_solicitud:**  Id de la solicitud del BCCR
        * **documento:** Documento firmado
        * **fue_exitosa:** si fue exitosa la firma
        * **codigo_error:** código de error
        * **hash_docfirmado:** Hash del documento ya firmado

    No requiere retornar nada

    """
    logdata = data
    if not settings.LOGGING_ENCRYPTED_DATA:
        logdata = {k: v for k, v in data.items() if k != 'documento'}
    logger.debug("Receptor: reciba notificación %r" %
                 (logdata,))

    for model in DATAREQUEST:
        request = model.objects.filter(
            id_transaction=data['id_solicitud']).first()
        if request is not None:
            break

    if request is None:
        logger.warning("Receptor: solicitud no encontrada %r" % (data, ))
        return

    logger.debug(str(type(request))+" " + str(data['id_solicitud'])
                 + " == " + str(request.status) + " --> "
                 + str(data['codigo_error']))
    request.status = data['codigo_error']
    request.status_text = get_text_representation(
        ERRORES_AL_NOTIFICAR_FIRMA,  data['codigo_error'])
    request.received_notification = True
    request.sign_document = get_document(data['documento'])
    request.hash_docsigned = get_hashsum_b64(data['hash_docfirmado'])
    request.hash_id_docsigned = data['hash_id']
    request.save()

    if hasattr(request, 'institution'):
        if not request.institution.administrative_institution:
            send_notification(
                request, encrypt_method=get_encrypt_method(request))


def valide_servicio():
    """
    Valida el si el servicio está disponible

    :returns:
        True si el servicio está disponible, 
        False si no lo está
    """

    dev = True
    logger.debug("Receptor: reciba notificación %r" %
                 (dev, ))
    return dev
