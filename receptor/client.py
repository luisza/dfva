'''
Created on 26 jul. 2017

@author: luis
'''

import logging
from receptor.notify import send_notification
from pyfva.constants import get_text_representation,\
    ERRORES_AL_NOTIFICAR_FIRMA

DATAREQUEST = []

try:
    from institution.models import AuthenticateDataRequest, SignDataRequest
    DATAREQUEST += [AuthenticateDataRequest, SignDataRequest]
except:
    pass

try:
    from person.models import AuthenticatePersonDataRequest, SignPersonDataRequest
    DATAREQUEST += [AuthenticatePersonDataRequest, SignPersonDataRequest]
except:
    pass
logger = logging.getLogger('dfva')


def get_encrypt_method(datarequest):
    encrypt_method = 'aes_eax'
    if isinstance(datarequest, AuthenticateDataRequest):
        encrypt_method = datarequest.authenticaterequest.encrypt_method
    elif isinstance(datarequest, SignDataRequest):
        encrypt_method = datarequest.signrequest.encrypt_method
    return encrypt_method


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

    for model in DATAREQUEST:
        request = model.objects.filter(
            id_transaction=data['id_solicitud']).first()
        if request is not None:
            break

    if request is None:
        logger.warning("Receptor: solicitud no encontrada %r" % (data, ))
        return

    request.status = data['codigo_error']
    request.status_text = get_text_representation(
        ERRORES_AL_NOTIFICAR_FIRMA,  data['codigo_error'])
    request.received_notification = True
    request.sign_document = data['documento']
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
