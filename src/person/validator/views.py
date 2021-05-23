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


class ValidateCertificatePersonViewSet(mixins.CreateModelMixin, GenericViewSet):
    """
    Valida si un certificado de la jerarquía nacional es válido.

    ::

      POST /person/validate_certificate

    Solicita una de un certificado de autenticación para un usuario

    Los valores a suministrar en el parámetro data son:

    * **person:** Identificación de la persona validante,
    * **document:** Archivo en base64 del certificado,
    * **request_datetime:** Hora de petición en formato '%Y-%m-%d %H:%M:%S', osea  '2006-10-25 14:30:59'
    * **format** Debe ser siempre "certificate"

    Data es un diccionario, osea un objeto de tipo clave -> valor

    Los valores devueltos son:

    * **identification:**  Identificación del suscriptor
    * **request_datetime:**  Hora de recepción de la solicitud
    * **code:** Código de identificación de la transacción (no es el mismo que el que se muestra en al usuario en firma)
    * **status:** Estado de la solicitud
    * **codigo_de_error:**  Códigos de error del certificado, si existen
    * **full_name:**  Nombre completo del suscriptor
    * **start_validity:**  Inicio de la vigencia del certificado
    * **end_validity:**  Fin de la vigencia del certificado
    * **was_successfully:**  Si la verificación del certificado fue exitosa

    **Nota:**  Si la validación del certificado no fue exitosa, entonces los campos de identificación, nombre_completo, inicio_vigencia,
    fin_vigencia deben ignorase o son nulos.

    """
    serializer_class = ValidatePersonCertificate_Request_Serializer
    queryset = ValidatePersonCertificateRequest.objects.all()
    response_class = ValidatePersonCertificateRequest_Response_Serializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]


class ValidateDocumentPersonViewSet(mixins.CreateModelMixin, GenericViewSet):
    """
    Solicita una verificación de firma  de un documento

    ::

      POST /person/validate_document/



    Los valores a suministrar en el parámetro data son:

    * **person:** Identificación de la persona validante,
    * **document:** Archivo en base64 del certificado,
    * **format:** Formato del documento a validar disponibles (cofirma, contrafirma, msoffice, odf)
    * **request_datetime:** Hora de petición en formato '%Y-%m-%d %H:%M:%S', osea  '2006-10-25 14:30:59'

    Data es un diccionario, osea un objeto de tipo clave -> valor

    Los valores devueltos son:

    * **identification:**  Identificación del suscriptor
    * **request_datetime:**  Hora de recepción de la solicitud
    * **code:** Código de identificación de la transacción (no es el mismo que el que se muestra en al usuario en firma)
    * **status:** Estado de la solicitud
    * **status_text:**  Descripción en texto del estado
    * **was_successfully:**  Si la verificación del certificado fue exitosa
    * **validation_data**  Contiene la información de la validación en un diccionario con los siguientes campos

    **firmas:** Lista de firmas presentes en el documento, una firma de ejemplo podría ser algo así

    ::

         {'es_valida': True, 'es_avanzada': True, 'error': False, 'detalle_de_error': '',
        'garantia_de_integridad_y_autenticidad': True,
        'garantia_de_validez_tiempo': [0, 'Tiene Garantía'],
        'detalle': {'integridad': {'estado': False, 'se_evalua': True, 'respuesta': 'ok', 'codigo': 1},
        'jerarquia_de_confianza': {'estado': 0, 'se_evalua': True, 'respuesta': 'ok', 'codigo': 1},
        'vigencia': {'estado': False, 'se_evalua': True, 'respuesta': 'ok', 'codigo': 1},
        'tipo_de_certificado': {'estado': 0, 'se_evalua': True, 'respuesta': 'ok', 'codigo': 1},
        'revocacion': {'estado': 0, 'se_evalua': True, 'respuesta': 'ok', 'codigo': 1},
        'fecha_de_firma': {'estado': False, 'se_evalua': True, 'respuesta': 'ok',
                            'codigo': 1, 'fecha_de_estama': '2021-05-20T00:00:00Z'}},
         'autoria_del_firmante': {'nombre': 'Joan Lucas Arce', 'identificacion': '0408880888',
                                   'tiene_autoria': True}}

    **resumen:** Resumen de las firmas (una versión con menos campos de las firmas)

    ::

        {'firmante': 'Luis Madrigal Viquez', 'identificacion': '0208880888',
        'garantia_de_integridad_y_autenticidad': True, 'garantia_validez_en_el_tiempo': True,
        'resultado': 0, 'fecha_estampa_de_tiempo': '2021-05-20T23:30:16Z',
        'tipo_identificacion': 0, 'tiene_fecha_estampa_de_tiempo': True}

    **errores:** Cadena de texto con mensajes de error presentes en las firmas del documento

    """
    serializer_class = ValidatePersonDocument_Request_Serializer
    queryset = ValidatePersonDocumentRequest.objects.all()
    response_class = ValidatePersonDocumentRequest_Response_Serializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]


class ValidateSubscriptorPersonViewSet(mixins.RetrieveModelMixin,  GenericViewSet):
    """
    Verifica si una persona está conectada (es contactable por el BCCR).

    ::

      POST /person/validate_suscriptor/

    Los valores a suministrar en el parámetro data son:

    * **person:** Identificación de la persona validante,
    * **identification:** Identificación de la persona a buscar,
    * **request_datetime:** Hora de petición en formato '%Y-%m-%d %H:%M:%S', osea  '2006-10-25 14:30:59'

    Data es un diccionario, osea un objeto de tipo clave -> valor

    **Retorna:**
        **is_connected:** True si la persona está conectada, false si no lo está
    """

    serializer_class = SuscriptorPerson_Serializer
    queryset = ValidatePersonCertificateRequest.objects.all()

    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def retrieve(self, request, *args, **kwargs):
        serializer = self.get_serializer()
        dev = serializer.call_BCCR({'identification': kwargs['pk']})
        return Response({'is_connected': dev})
