'''
Created on 12 sep. 2017

@author: luisza
'''
from rest_framework.decorators import detail_route, list_route
from django.utils import timezone
from corebase.views import ViewSetBase
from rest_framework import viewsets
from rest_framework.response import Response
from institution.signer.serializer import Sign_Request_Serializer,\
    Sign_Response_Serializer
from institution.models import SignRequest
from corebase.logging import get_ip, get_log_institution_information
from pyfva.constants import get_text_representation
import pyfva
import logging


logger = logging.getLogger('dfva')


class SignRequestViewSet(ViewSetBase,
                         viewsets.GenericViewSet):

    serializer_class = Sign_Request_Serializer
    queryset = SignRequest.objects.all()
    response_class = Sign_Response_Serializer

    @list_route(methods=['post'])
    def institution(self, request, *args, **kwargs):
        """
        ::

          POST /sign/institution/

        Solicita una firma de un documento xml, odf o msoffice para un usuario 

        Los valores a suministrar en el parámetro data son:

        * **institution:** uid de la institucion ver code en detalles de institución,
        * **notification_url:** URL para la notificación (debe estar inscrita) o N/D si marca falso en not_webapp,
        * **document:** Archivo en base64, 
        * **format:** tipo de archivo (xml_cofirma, xml_contrafirma, odf, msoffice), 
        * **algorithm_hash:** algoritmo usado para calcular hash, 
        * **document_hash:** hash del documento,
        * **resumen:** Información de ayuda acerca del documento,      
        * **identification:** Identificación de la persona a autenticar,
        * **request_datetime:** Hora de petición en formato '%Y-%m-%d %H:%M:%S', osea  '2006-10-25 14:30:59'

        Data es un diccionario, osea un objeto de tipo clave -> valor

        Los valores devueltos son: 

        * **expiration_datetime:** hora final de validez
        * **request_datetime:** Hora de recepción de la solicitud
        * **id_transaction:** Id de trasnacción en el FVA del BCCR
        * **sign_document:** Normalmente None, es un campo para almacenar el documento, pero no se garantiza que venga el documento firmado
        * **status:** Código de error de la transacción
        * **status_text** Descripción para humanos del código de error
        * **identification:** Identificador del suscriptor
        * **code:** Código para mostrar al usuario
        * **received_notification** True si la autenticación ha sido procesada, False si está esperando al usuario

        """

        ip = get_ip(request)
        logger.debug('Sign: Create Institution %s %r' %
                     (ip, request.data))
        logger.info('Sign: Create Institution %s %s %s %s' %
                    get_log_institution_information(request))
        return self._create(request, *args, **kwargs)

    @detail_route(methods=['post'])
    def institution_show(self, request, *args, **kwargs):
        """
        ::

          POST /sign/{id_transaction}/institution_show/

        Verifica la firma dado un código y si respectiva identificación

        Los valores a suministrar en el parámetro data son:

        * **institution:** uid de la institucion ver code en detalles de institución,
        * **notification_url:** URL para la notificación (debe estar inscrita) o N/D si marca falso en not_webapp,   
        * **identification:** Identificación de la persona a autenticar,
        * **request_datetime:** Hora de petición en formato '%Y-%m-%d %H:%M:%S', osea  '2006-10-25 14:30:59'

        Data es un diccionario, osea un objeto de tipo clave -> valor

        **id_transaction** Corresponde al id de la trasnacción del BCCR

        Los valores devueltos son: 

        * **expiration_datetime:** hora final de validez
        * **request_datetime:** Hora de recepción de la solicitud
        * **id_transaction:** Id de trasnacción en el FVA del BCCR
        * **sign_document:** Normalmente None, es un campo para almacenar el documento, pero no se garantiza que venga el documento firmado
        * **status:** Código de error de la transacción
        * **status_text** Descripción para humanos del código de error
        * **identification:** Identificador del suscriptor
        * **code:** Código para mostrar al usuario
        * **received_notification** True si la autenticación ha sido procesada, False si está esperando al usuario

        """
        ip = get_ip(request)
        logger.debug('Sign: Show Institution %s %r' %
                     (ip, request.data))
        logger.info('Sign: Show Institution %s %s %s %s' %
                    get_log_institution_information(request))
        return self.show(request, *args, **kwargs)

    @detail_route(methods=['post'])
    def institution_delete(self, request, *args, **kwargs):
        """
        ::

          POST /sign/{id_transaction}/institution_delete/

        Elimina una petición de firma dado un código de transacción del BCCR

        Los valores a suministrar en el parámetro data son:

        * **institution:** uid de la institucion ver code en detalles de institución,
        * **notification_url:** URL para la notificación (debe estar inscrita) o N/D si marca falso en not_webapp,   
        * **request_datetime:** Hora de petición en formato '%Y-%m-%d %H:%M:%S', osea  '2006-10-25 14:30:59'

        Data es un diccionario, osea un objeto de tipo clave -> valor

        **id_transaction** Corresponde al id de la trasacción del BCCR

        Los valores devueltos son: 
       
        * **result** True/False si se eliminó la petición o no
        
        """
        ip = get_ip(request)
        logger.debug('Sign: Delete Institution %s %r' %
                     (ip, request.data))
        logger.info('Sign: Delete Institution %s %s %s %s' %
                    get_log_institution_information(request))
        return self.delete(request, *args, **kwargs)



    def get_error_response(self, serializer):
        dev = {
            'code': 'N/D',
            'status': 2,
            'status_text': get_text_representation(pyfva.constants.ERRORES_AL_SOLICITAR_FIRMA, 2),
            'identification': 'N/D',
            'id_transaction': 0,
            'request_datetime': timezone.now(),
            'sign_document': None,
            'expiration_datetime': None,
            'received_notification': False,
            'error_info': serializer._errors
        }
        logger.debug('Sign: ERROR Institution %r' %
                     (dev, ))
        return Response(self.get_encrypted_response(dev, serializer))
