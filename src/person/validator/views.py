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
@date: 13/9/2017
@author: Luis Zarate Montero
@contact: luis.zarate@solvosoft.com
@license: GPLv3
'''
from rest_framework.decorators import action
from rest_framework.response import Response

from corebase.views import ViewSetBase, BaseSuscriptor
from rest_framework import viewsets
from person.validator.serializer import \
    ValidatePersonCertificate_Request_Serializer,\
    ValidatePersonCertificateRequest_Response_Serializer,\
    ValidatePersonDocument_Request_Serializer,\
    ValidatePersonDocumentRequest_Response_Serializer,\
    SuscriptorPerson_Serializer
from person.models import ValidatePersonCertificateRequest,\
    ValidatePersonDocumentRequest

from corebase.logging import get_ip, get_log_person_information
from pyfva.constants import ERRORES_VALIDA_CERTIFICADO,\
    ERRORES_VALIDAR_XMLCOFIRMA
import logging
from django.conf import settings
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework import mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet
logger = logging.getLogger(settings.DEFAULT_LOGGER_NAME)


class ValidateCertificatePersonViewSet(mixins.RetrieveModelMixin, mixins.CreateModelMixin, mixins.DestroyModelMixin,
                                       GenericViewSet):
    serializer_class = ValidatePersonCertificate_Request_Serializer
    queryset = ValidatePersonCertificateRequest.objects.all()
    response_class = ValidatePersonCertificateRequest_Response_Serializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]


class ValidateDocumentPersonViewSet(mixins.RetrieveModelMixin, mixins.CreateModelMixin, mixins.DestroyModelMixin,
                                       GenericViewSet):
    serializer_class = ValidatePersonDocument_Request_Serializer
    queryset = ValidatePersonDocumentRequest.objects.all()
    response_class = ValidatePersonDocumentRequest_Response_Serializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]


class ValidateSubscriptorPersonViewSet(mixins.RetrieveModelMixin,  GenericViewSet):
    serializer_class = SuscriptorPerson_Serializer
    queryset = ValidatePersonCertificateRequest.objects.all()

    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def retrieve(self, request, *args, **kwargs):
        serializer = self.get_serializer()
        dev = serializer.call_BCCR({'identification': kwargs['pk']})
        return Response({'is_connected': dev})

# class ValidatePersonViewSet(ViewSetBase, viewsets.GenericViewSet):
#     serializer_class = ValidatePersonCertificate_Request_Serializer
#     queryset = ValidatePersonCertificateRequest.objects.all()
#     response_class = ValidatePersonCertificateRequest_Response_Serializer
#
#     @authentication_classes([TokenAuthentication])
#     @permission_classes([IsAuthenticated])
#     @action(detail=False, methods=['post'])
#     def person_certificate(self, request, *args, **kwargs):
#         """
#         ::
#
#           POST /validate/person_certificate/
#
#         Solicita una de un certificado de autenticación para un usuario
#
#         Los valores a suministrar en el parámetro data son:
#
#         * **person:** Identificación de la persona validante,
#         * **document:** Archivo en base64 del certificado,
#         * **request_datetime:** Hora de petición en formato '%Y-%m-%d %H:%M:%S', osea  '2006-10-25 14:30:59'
#
#         Data es un diccionario, osea un objeto de tipo clave -> valor
#
#         Los valores devueltos son:
#
#         * **identification:**  Identificación del suscriptor
#         * **request_datetime:**  Hora de recepción de la solicitud
#         * **code:** Código de identificación de la transacción (no es el mismo que el que se muestra en al usuario en firma)
#         * **status:** Estado de la solicitud
#         * **codigo_de_error:**  Códigos de error del certificado, si existen
#         * **full_name:**  Nombre completo del suscriptor
#         * **start_validity:**  Inicio de la vigencia del certificado
#         * **end_validity:**  Fin de la vigencia del certificado
#         * **was_successfully:**  Si la verificación del certificado fue exitosa
#
#         **Nota:**  Si la validación del certificado no fue exitosa, entonces los campos de identificación, nombre_completo, inicio_vigencia,
#         fin_vigencia deben ignorase o son nulos.
#
#         """
#         ip = get_ip(request)
#         logger.debug('Validator: Certificate Person %s %r' %
#                      (ip, request.data))
#         logger.info('Validator: Certificate Person %s %s %s %s' %
#                     get_log_person_information(request))
#         self.DEFAULT_ERROR = ERRORES_VALIDA_CERTIFICADO
#         return self._create(request, *args, **kwargs)
#
#     @authentication_classes([TokenAuthentication])
#     @permission_classes([IsAuthenticated])
#     @action(detail=False, methods=['post'])
#     def person_document(self, request, *args, **kwargs):
#         """
#         ::
#
#           POST /validate/person_document/
#
#         Solicita una verificación de firma  de un documento xml
#
#         Los valores a suministrar en el parámetro data son:
#
#         * **person:** Identificación de la persona validante,
#         * **document:** Archivo en base64 del certificado,
#         * **format:** Formato del documento a validar disponibles (cofirma, contrafirma, msoffice, odf)
#         * **request_datetime:** Hora de petición en formato '%Y-%m-%d %H:%M:%S', osea  '2006-10-25 14:30:59'
#
#         Data es un diccionario, osea un objeto de tipo clave -> valor
#
#         Los valores devueltos son:
#
#         * **identification:**  Identificación del suscriptor
#         * **request_datetime:**  Hora de recepción de la solicitud
#         * **code:** Código de identificación de la transacción (no es el mismo que el que se muestra en al usuario en firma)
#         * **status:** Estado de la solicitud
#         * **status_text:**  Descripción en texto del estado
#         * **warnings:** Lista de advertencias
#         * **errors:** Lista de errores encontrados en el documento del tipo [ {'codigo': 'codigo','descripcion': 'descripción'}, ... ]
#         * **signers:** Lista con la información de los firmantes [ {'identification': '08-8888-8888', 'full_name': 'nombre del suscriptor', 'signature_date': timezone.now()}, ... ]
#         * **was_successfully:**  Si la verificación del certificado fue exitosa
#
#         **Nota:**  Si la validación del documento no fue exitosa, entonces los campos de firmantes deben ignorase o son nulos.
#
#         """
#
#         ip = get_ip(request)
#         logger.debug('Validator: Document Person %s %r' %
#                      (ip, request.data))
#         logger.info('Validator: Document Person %s %s %s %s' %
#                     get_log_person_information(request))
#         self.serializer_class = ValidatePersonDocument_Request_Serializer
#         self.queryset = ValidatePersonDocumentRequest.objects.all()
#         self.response_class = ValidatePersonDocumentRequest_Response_Serializer
#         self.DEFAULT_ERROR = ERRORES_VALIDAR_XMLCOFIRMA
#         return self._create(request, *args, **kwargs)
#
#
# class ValidateSubscriptorPersonViewSet(BaseSuscriptor, viewsets.GenericViewSet):
#     serializer_class = SuscriptorPerson_Serializer
#     queryset = ValidatePersonCertificateRequest.objects.all()
#
#     @authentication_classes([TokenAuthentication])
#     @permission_classes([IsAuthenticated])
#     @action(detail=False, methods=['post'])
#     def person_suscriptor_connected(self, request, *args, **kwargs):
#         """
#         ::
#
#           POST /validate/person_suscriptor_connected/
#
#         Verifica si una persona está conectada (es contactable por el BCCR).
#
#         Los valores a suministrar en el parámetro data son:
#
#         * **person:** Identificación de la persona validante,
#         * **identification:** Identificación de la persona a buscar,
#         * **request_datetime:** Hora de petición en formato '%Y-%m-%d %H:%M:%S', osea  '2006-10-25 14:30:59'
#
#         Data es un diccionario, osea un objeto de tipo clave -> valor
#
#         **Retorna:**
#             **is_connected:** True si la persona está conectada, false si no lo está
#         """
#         ip = get_ip(request)
#         logger.debug('Connected:  person %s %r' % (ip, request.data))
#         logger.info('Connected:  person %s %s %s %s' % get_log_person_information(request))
#         return self._create(request,  *args, **kwargs)
