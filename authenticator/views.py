from rest_framework import viewsets
from rest_framework.response import Response

from authenticator.models import AuthenticateRequest
from authenticator.serializer import Authenticate_Request_Serializer,\
    Authenticate_Response_Serializer
from django.utils import timezone
import logging
from rest_framework.decorators import detail_route, list_route
from corebase.views import ViewSetBase

# Person
from authenticator.models import AuthenticatePersonRequest
from authenticator.serializer import Authenticate_Person_Response_Serializer,\
    Authenticate_Person_Request_Serializer
import pyfva
from pyfva.constants import get_text_representation
from corebase.logging import get_ip, get_log_institution_information,\
    get_log_person_information


logger = logging.getLogger('dfva')

# Create your views here.


class AuthenticateRequestViewSet(ViewSetBase,
                                 viewsets.GenericViewSet):
    serializer_class = Authenticate_Request_Serializer
    queryset = AuthenticateRequest.objects.all()
    response_class = Authenticate_Response_Serializer

    @list_route(methods=['post'])
    def institution(self, request, *args, **kwargs):
        """
        ::
        
          POST /authenticate/institution/

        Solicita una petición de autenticación para un usuario 

        Los valores a suministrar en el parámetro data son:

        * **institution:** uid de la institucion ver code en detalles de institución,
        * **notification_url:** URL para la notificación (debe estar inscrita) o N/D si marca falso en not_webapp,
        * **identification:** Identificación de la persona a autenticar,
        * **request_datetime:** Hora de petición en formato '%Y-%m-%d %H:%M:%S', osea  '2006-10-25 14:30:59'

        Data es un diccionario, osea un objeto de tipo clave -> valor

        Los valores devueltos son: 

        * **expiration_datetime:** hora final de validez
        * **request_datetime:** Hora de recepción de la solicitud
        * **id_transaction:** Id de trasnacción en el FVA del BCCR
        * **status:** Código de error de la transacción
        * **identification:** Identificador del suscriptor
        * **code:** Código para mostrar al usuario
        * **received_notification** True si la autenticación ha sido procesada, False si está esperando al usuario

        """
        ip = get_ip(request)
        logger.debug('Authentication: Create Institution %s %r' %
                     (ip, request.data))
        logger.info('Authentication: Create Institution %s %s %s %s' %
                    get_log_institution_information(request))
        return self._create(request, *args, **kwargs)

    @detail_route(methods=['post'])
    def institution_show(self, request, *args, **kwargs):
        """
        ::
        
          POST /authenticate/{code}/institution_show/

        Solicita el estado de una petición de autenticación para un usuario 

        Los valores a suministrar en el parámetro data son:

        * **institution:** uid de la institucion ver code en detalles de institución,
        * **notification_url:** URL para la notificación (debe estar inscrita) o N/D si marca falso en not_webapp,
        * **identification:** Identificación de la persona a autenticar,
        * **request_datetime:** Hora de petición en formato '%Y-%m-%d %H:%M:%S', osea  '2006-10-25 14:30:59'

        Data es un diccionario, osea un objeto de tipo clave -> valor

        Los valores devueltos son: 

        * **expiration_datetime:** hora final de validez
        * **request_datetime:** Hora de recepción de la solicitud
        * **id_transaction:** Id de trasnacción en el FVA del BCCR
        * **status:** Código de error de la transacción
        * **identification:** Identificador del suscriptor
        * **code:** Código para mostrar al usuario
        * **received_notification** True si la autenticación ha sido procesada, False si está esperando al usuario

        """
        ip = get_ip(request)
        logger.debug('Authentication: Show Institution %s %r' %
                     (ip, request.data))
        logger.info('Authentication: Show Institution %s %s %s %s' %
                    get_log_institution_information(request))
        return self.show(request, *args, **kwargs)

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
        logger.debug('Authentication: Error Institution %r' %
                     (dev, ))

        return Response(self.get_encrypted_response(dev, serializer))


class AuthenticatePersonRequestViewSet(ViewSetBase,
                                       viewsets.GenericViewSet):
    serializer_class = Authenticate_Person_Request_Serializer
    queryset = AuthenticatePersonRequest.objects.all()
    response_class = Authenticate_Person_Response_Serializer

    @list_route(methods=['post'])
    def person(self, request, *args, **kwargs):
        """
        ::

          POST /authenticate/person/
        
        Solicita una petición de autenticación para un usuario 

        Los valores a suministrar en el parámetro data son:

        * **person:** identificación de la persona solicitante de autenticación,
        * **identification:** Identificación de la persona a autenticar,
        * **request_datetime:** Hora de petición en formato '%Y-%m-%d %H:%M:%S', osea  '2006-10-25 14:30:59'

        Data es un diccionario, osea un objeto de tipo clave -> valor

        Los valores devueltos son: 

        * **expiration_datetime:** hora final de validez
        * **request_datetime:** Hora de recepción de la solicitud
        * **id_transaction:** Id de trasnacción en el FVA del BCCR
        * **status:** Código de error de la transacción
        * **identification:** Identificador del suscriptor
        * **code:** Código para mostrar al usuario
        * **received_notification** True si la autenticación ha sido procesada, False si está esperando al usuario
        """
        ip = get_ip(request)
        logger.debug('Authentication: Create Person %s %r' %
                     (ip, request.data))
        logger.info('Authentication: Create Person %s %s %s %s' %
                    get_log_person_information(request))
        return self._create(request, *args, **kwargs)

    @detail_route(methods=['post'])
    def person_show(self, request, *args, **kwargs):
        """
        ::

          POST /authenticate/{code}/person_show/
        
        Solicita un estado de la solicitud de autenticación para un usuario 

        Los valores a suministrar en el parámetro data son:

        * **person:** identificación de la persona solicitante de autenticación,
        * **identification:** Identificación de la persona a autenticar,
        * **request_datetime:** Hora de petición en formato '%Y-%m-%d %H:%M:%S', osea  '2006-10-25 14:30:59'

        Data es un diccionario, osea un objeto de tipo clave -> valor

        Los valores devueltos son: 

        * **expiration_datetime:** hora final de validez
        * **request_datetime:** Hora de recepción de la solicitud
        * **id_transaction:** Id de trasnacción en el FVA del BCCR
        * **status:** Código de error de la transacción
        * **identification:** Identificador del suscriptor
        * **code:** Código para mostrar al usuario
        * **received_notification** True si la autenticación ha sido procesada, False si está esperando al usuario
        """
        ip = get_ip(request)
        logger.debug('Authentication: Show Person %s %r' %
                     (ip, request.data))
        logger.info('Authentication: Show Person %s %s %s %s' %
                    get_log_person_information(request))
        return self.show(request, *args, **kwargs)

    def get_error_response(self, serializer):
        dev = {
            'code': 'N/D',
            'status': 2,
            'identification': 'N/D',
            'id_transaction': 0,
            'request_datetime': timezone.now(),
            'sign_document': None,
            'expiration_datetime': None,
            'received_notification': False,
            'error_info': serializer._errors
        }
        logger.debug('Authentication: Error Person %r' %
                     (dev, ))

        return Response(self.get_encrypted_response(dev, serializer))
