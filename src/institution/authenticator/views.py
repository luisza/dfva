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
@author: Universidad de Costa Rica
@maintainer: Luis Zarate Montero
@contact: luis.zarate@solvosoft.com
@license: GPLv3
'''

from rest_framework import viewsets
from rest_framework.response import Response


from django.utils import timezone
import logging
from rest_framework.decorators import detail_route, list_route
from corebase.views import ViewSetBase
import pyfva
from pyfva.constants import get_text_representation
from corebase.logging import get_ip, get_log_institution_information
from institution.authenticator.serializer import \
    Authenticate_Request_Serializer,\
    Authenticate_Response_Serializer
from institution.models import AuthenticateRequest
from django.conf import settings

logger = logging.getLogger(settings.DEFAULT_LOGGER_NAME)

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
        * **encrypt_method:** (opcional, default: "aes_eax") Método de encripción de segunda fase. ("aes_eax", "aes-256-cfb")  

        Data es un diccionario, osea un objeto de tipo clave -> valor

        Los valores devueltos son: 

        * **expiration_datetime:** hora final de validez
        * **request_datetime:** Hora de recepción de la solicitud
        * **id_transaction:** Id de trasnacción en el FVA del BCCR
        * **status:** Código de error de la transacción
        * **status_text** Descripción para humanos del código de error
        * **identification:** Identificador del suscriptor
        * **code:** Código para mostrar al usuario
        * **received_notification** True si la autenticación ha sido procesada, False si está esperando al usuario

        """
        ip = get_ip(request)
        if settings.LOGGING_ENCRYPTED_DATA:
            logger.debug('Authentication: Create Institution %s %r' %
                         (ip, request.data))
        logger.info('Authentication: Create Institution %s %s %s %s' %
                    get_log_institution_information(request))
        return self._create(request, *args, **kwargs)

    @detail_route(methods=['post'])
    def institution_show(self, request, *args, **kwargs):
        """
        ::

          POST /authenticate/{id_transaction}/institution_show/

        Solicita el estado de una petición de autenticación para un usuario 

        Los valores a suministrar en el parámetro data son:

        * **institution:** uid de la institucion ver code en detalles de institución,
        * **notification_url:** URL para la notificación (debe estar inscrita) o N/D si marca falso en not_webapp,
        * **request_datetime:** Hora de petición en formato '%Y-%m-%d %H:%M:%S', osea  '2006-10-25 14:30:59'

        Data es un diccionario, osea un objeto de tipo clave -> valor

        **id_transaction** Corresponde al id de la trasnacción del BCCR

        Los valores devueltos son: 

        * **expiration_datetime:** hora final de validez
        * **request_datetime:** Hora de recepción de la solicitud
        * **id_transaction:** Id de trasnacción en el FVA del BCCR
        * **status:** Código de error de la transacción
        * **status_text** Descripción para humanos del código de error
        * **identification:** Identificador del suscriptor
        * **code:** Código para mostrar al usuario
        * **received_notification** True si la autenticación ha sido procesada, False si está esperando al usuario

        """
        ip = get_ip(request)
        if settings.LOGGING_ENCRYPTED_DATA:
            logger.debug('Authentication: Show Institution %s %r' %
                         (ip, request.data))
        logger.info('Authentication: Show Institution %s %s %s %s' %
                    get_log_institution_information(request))
        return self.show(request, *args, **kwargs)

    def get_error_response(self, serializer):
        dev = {
            'code': 'N/D',
            'status': 2,
            'status_text': get_text_representation(
                pyfva.constants.ERRORES_AL_SOLICITAR_FIRMA, 1),
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

    @detail_route(methods=['post'])
    def institution_delete(self, request, *args, **kwargs):
        """
        ::

          POST /authenticate/{id_transaction}/institution_delete/

        Elimina una petición de autenticación para un usuario 

        Los valores a suministrar en el parámetro data son:

        * **institution:** uid de la institucion ver code en detalles de institución,
        * **notification_url:** URL para la notificación (debe estar inscrita) o N/D si marca falso en not_webapp,
        * **request_datetime:** Hora de petición en formato '%Y-%m-%d %H:%M:%S', osea  '2006-10-25 14:30:59'

        Data es un diccionario, osea un objeto de tipo clave -> valor

        **id_transaction** Corresponde al id de la trasnacción del BCCR

        Los valores devueltos son: 

        * **result** True/False si se eliminó la petición o no

        """
        ip = get_ip(request)
        if settings.LOGGING_ENCRYPTED_DATA:
            logger.debug('Authentication: Delete Institution request %s %r' %
                         (ip, request.data))
        logger.info('Authentication: Delete Institution request %s %s %s %s' %
                    get_log_institution_information(request))
        return self.delete(request, *args, **kwargs)
