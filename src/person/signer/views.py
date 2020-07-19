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
@date: 14/4/2017
@author: Luis Zarate Montero
@contact: luis.zarate@solvosoft.com
@license: GPLv3
'''

import logging

from django.conf import settings
from rest_framework import mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from person.models import SignPersonRequest
from person.signer.serializer import Sign_Person_Request_Serializer, \
    Sign_Person_Response_Serializer

logger = logging.getLogger(settings.DEFAULT_LOGGER_NAME)



class SignPersonView(mixins.RetrieveModelMixin, mixins.CreateModelMixin, mixins.DestroyModelMixin, GenericViewSet):
    serializer_class = Sign_Person_Request_Serializer
    queryset = SignPersonRequest.objects.all()
    response_class = Sign_Person_Response_Serializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     id_transaction = self.request.query_params.get('id_transaction', None)
    #     if id_transaction is not None:
    #         queryset = queryset.filter(id_transaction=id_transaction)
    #     else:
    #         queryset = queryset.none()
    #     return queryset

    def retrieve(self, request, *args, **kwargs):
        self.serializer_class = self.response_class
        return super().retrieve(request, *args, **kwargs)



# class SignPersonRequestViewSet(ViewSetBase,
#                                viewsets.GenericViewSet):
#     serializer_class = Sign_Person_Request_Serializer
#     queryset = SignPersonRequest.objects.all()
#     response_class = Sign_Person_Response_Serializer
#
#     @authentication_classes([TokenAuthentication])
#     @permission_classes([IsAuthenticated])
#     @action(detail=False, methods=['post'])
#     def person(self, request, *args, **kwargs):
#         """
#         ::
#
#           POST /sign/person/
#
#         Solicita una firma de un documento xml, odf o msoffice para un usuario
#
#         Los valores a suministrar en el parámetro data son:
#
#         * **person:** identificación de la persona solicitante de firma,
#         * **notification_url:** URL para la notificación (debe estar inscrita) o N/D si marca falso en not_webapp,
#         * **document:** Archivo en base64,
#         * **format:** tipo de archivo (xml_cofirma,xml_contrafirma, odf, msoffice),
#         * **algorithm_hash:** algoritmo usado para calcular hash,
#         * **document_hash:** hash del documento,
#         * **resumen:** Información de ayuda acerca del documento,
#         * **identification:** Identificación de la persona a firmar,
#         * **request_datetime:** Hora de petición en formato '%Y-%m-%d %H:%M:%S', osea  '2006-10-25 14:30:59'
#
#         Data es un diccionario, osea un objeto de tipo clave -> valor
#
#         Los valores devueltos son:
#
#         * **expiration_datetime:** hora final de validez
#         * **request_datetime:** Hora de recepción de la solicitud
#         * **id_transaction:** Id de trasnacción en el FVA del BCCR
#         * **sign_document:** Normalmente None, es un campo para almacenar el documento, pero no se garantiza que venga el documento firmado
#         * **status:** Código de error de la transacción
#         * **identification:** Identificador del suscriptor
#         * **code:** Código para mostrar al usuario
#         * **received_notification** True si la autenticación ha sido procesada, False si está esperando al usuario
#
#         """
#         ip = get_ip(request)
#         logger.debug('Sign: Create Person %s %r' %
#                      (ip, request.data))
#         logger.info('Sign: Create Person %s %s %s %s' %
#                     get_log_person_information(request))
#         return self._create(request, *args, **kwargs)
#
#     @authentication_classes([TokenAuthentication])
#     @permission_classes([IsAuthenticated])
#     @action(detail=True, methods=['post'])
#     def person_show(self, request, *args, **kwargs):
#         """
#         ::
#
#           POST /sign/{code}/person_show/
#
#         Verifica la firma dado un código y su respectiva identificación
#
#         Los valores a suministrar en el parámetro data son:
#
#         * **person:** identificación de la persona solicitante de firma,
#         * **identification:** Identificación de la persona a autenticar,
#         * **request_datetime:** Hora de petición en formato '%Y-%m-%d %H:%M:%S', osea  '2006-10-25 14:30:59'
#
#         Data es un diccionario, osea un objeto de tipo clave -> valor
#
#         Los valores devueltos son:
#
#         * **expiration_datetime:** hora final de validez
#         * **request_datetime:** Hora de recepción de la solicitud
#         * **id_transaction:** Id de trasnacción en el FVA del BCCR
#         * **sign_document:** Normalmente None, es un campo para almacenar el documento, pero no se garantiza que venga el documento firmado
#         * **status:** Código de error de la transacción
#         * **identification:** Identificador del suscriptor
#         * **code:** Código para mostrar al usuario
#         * **received_notification** True si la autenticación ha sido procesada, False si está esperando al usuario
#
#         """
#         ip = get_ip(request)
#         logger.debug('Sign: Show Person %s %r' %
#                      (ip, request.data))
#         logger.info('Sign: Show Person %s %s %s %s' %
#                     get_log_person_information(request))
#         return self.show(request, *args, **kwargs)
#
#     def get_error_response(self, serializer):
#         dev = {
#             'code': 'N/D',
#             'status': 2,
#             'status_text': get_text_representation(
#                 pyfva.constants.ERRORES_AL_SOLICITAR_FIRMA, 2),
#             'identification': 'N/D',
#             'id_transaction': 0,
#             'request_datetime': timezone.now(),
#             'sign_document': None,
#             'expiration_datetime': None,
#             'received_notification': False,
#             'error_info': serializer._errors
#         }
#         logger.debug('Sign: ERROR person %r' %
#                      (dev,))
#         return Response(self.get_encrypted_response(dev, serializer))
