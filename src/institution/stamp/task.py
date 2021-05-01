from django.utils import timezone

from institution.models import Institution, StampDataRequest
from pyfva.clientes.sellador import ClienteSellador
from django.conf import settings
from corebase import logger
from receptor.notify import send_notification


def stamp_call_bccr(pk, institution):
    log_sector='stamp'
    institution = Institution.objects.get(pk=institution)
    request = StampDataRequest.objects.get(pk=pk)
    metrics = request.system_metrics
    if metrics is None:
        logger.error({'message': "Stamp without metrics, maybe is a creation error", 'data': repr(request), 'location': __file__}, sector=log_sector)
        raise
    logger.debug({'message': "Stamp STATS", 'data': str(metrics), 'location': __file__}, sector=log_sector)
    stampclient = ClienteSellador(
        negocio=institution.bccr_bussiness,
        entidad=institution.bccr_entity,
    )

    metrics.start_bccr_call = timezone.now()
    if stampclient.validar_servicio():
        data = stampclient.firme(
            request.document,
            request.document_format,
            algoritmo_hash=request.algorithm_hash,
            hash_doc=request.document_hash,
            lugar=request.place,
            razon=request.reason,
            id_funcionalidad=request.id_functionality
        )
    else:
        logger.warning({'message': "Stamp BCCR not available", 'location': __file__}, sector=log_sector)
        data = stampclient.DEFAULT_ERROR

    request.signed_document = data['documento']
    request.status = data['codigo_error']
    request.status_text = data['texto_codigo_error']
    request.received_notification = True
    request.algorithm_hash = data['id_algoritmo_hash']
    request.was_successfully = data['fue_exitosa']
    request.hash_docsigned = data['hash_documento']
    request.save()
    logger.debug({'message': "Sign Stamp", 'data': data, 'location': __file__}, sector=log_sector)
    metrics.end_bccr_call = timezone.now()
    metrics.transaction_status = request.status
    metrics.transaction_status_text = request.status_text
    metrics.transaction_success = settings.DEFAULT_SUCCESS_BCCR == request.status
    metrics.save()
    setattr(request, 'id_transaction', request.pk)

    # this prevent circular imports
    from institution.stamp.serializer import Stamp_Response_Serializer
    send_notification(request, serializer=Stamp_Response_Serializer,
                      encrypt_method=request.stamprequest.encrypt_method)
