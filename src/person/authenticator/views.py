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

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated

from django.utils import timezone
import logging

from rest_framework.viewsets import GenericViewSet

from corebase.views import ViewSetBase
from corebase.logging import get_ip, get_log_person_information
from person.models import AuthenticatePersonRequest
from person.authenticator.serializer import \
    Authenticate_Person_Request_Serializer,\
    Authenticate_Person_Response_Serializer
from django.conf import settings

logger = logging.getLogger(settings.DEFAULT_LOGGER_NAME)

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import mixins

logger = logging.getLogger(settings.DEFAULT_LOGGER_NAME)



class AuthenticatePersonView(mixins.RetrieveModelMixin, mixins.CreateModelMixin, mixins.DestroyModelMixin,
                             GenericViewSet):
    """
    **Solucitud de autenticación de una persona**

    ::

      POST /person/authenticate/

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
    * **signed_document** Siempre es  None puesto que el documento todavía no se ha firmado a este punto
    * **duration**  Tiempo en segundos que dura la transacción

    **Solucitud de información de una transacción de autenticación**

    ::

      GET /person/authenticate/{transaction_id}/

    Solicita un estado de la solicitud de autenticación para un usuario

    Los valores a suministrar en el parámetro data son:

    * **transaction_id:** identificación de la transacción de autenticación de la que se requiere información

    Data es un diccionario, osea un objeto de tipo clave -> valor

    Los valores devueltos son:

    * **expiration_datetime:** hora final de validez
    * **request_datetime:** Hora de recepción de la solicitud
    * **id_transaction:** Id de trasnacción en el FVA del BCCR
    * **status:** Código de error de la transacción
    * **identification:** Identificador del suscriptor
    * **code:** Código para mostrar al usuario
    * **received_notification** True si la autenticación ha sido procesada, False si está esperando al usuario
    * **signed_document** Documento firmado en base64 o None si aún no se ha firmado la autenticación
    * **duration**  Tiempo en segundos que dura la transacción

    **Elimina la información de la transacción de autenticación**

    ::

      DELETE /person/authenticate/{transaction_id}/

    Los valores devueltos son:

        No tiene valores devueltos
    """


    serializer_class = Authenticate_Person_Request_Serializer
    queryset = AuthenticatePersonRequest.objects.all()
    response_class = Authenticate_Person_Response_Serializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def retrieve(self, request, *args, **kwargs):
        self.serializer_class = self.response_class
        return super().retrieve(request, *args, **kwargs)

