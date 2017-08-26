'''
Created on 26 jul. 2017

@author: luis
'''

import logging
from authenticator.models import AuthenticateDataRequest,\
    AuthenticatePersonDataRequest
from signer.models import SignDataRequest, SignPersonDataRequest
from receptor.notify import send_notification
logger = logging.getLogger('dfva')


def reciba_notificacion(data):
    """
    Recibe la notificación del BCCR

    :params data: Es un diccionario con los siguientes atributos

        * **id_solicitud:**  Id de la solicitud del BCCR
        * **documento:** Documento firmado
        * **fue_exitosa:** si fue exitosa la firma
        * **codigo_error:** código de error

    No requiere retornar nada

    """
    logger.debug("Receptor: reciba notificación %r" %
                 (data,))

    for model in [AuthenticateDataRequest,
                  AuthenticatePersonDataRequest,
                  SignDataRequest,
                  SignPersonDataRequest]:
        request = model.objects.filter(
            id_transaction=data['id_solicitud']).first()
        if request is not None:
            break

    if request is None:
        logger.warning("Receptor: solicitud no encontrada %r" % (data, ))
        return

    request.status = data['codigo_error']
    request.received_notification = True
    request.sign_document = data['documento']
    request.save()
    if hasattr(request, 'institution'):
        send_notification(request)


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
