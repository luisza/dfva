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

from django.utils import timezone
from corebase.views import ViewSetBase
from rest_framework import viewsets
from rest_framework.response import Response
from institution.stamp.serializer import Stamp_Request_Serializer,\
    Stamp_Response_Serializer
from institution.models import StampRequest
from corebase.logging import get_ip, get_log_institution_information
from pyfva.constants import get_text_representation
import pyfva
from django.conf import settings
from rest_framework.decorators import action

from corebase import logger


class StampRequestViewSet(ViewSetBase,
                         viewsets.GenericViewSet):

    serializer_class = Stamp_Request_Serializer
    queryset = StampRequest.objects.all()
    response_class = Stamp_Response_Serializer
    log_sector = 'stamp'

    @action(detail=False, methods=['post'])
    def institution(self, request, *args, **kwargs):
        """
        ::

          POST /stamp/institution/

        Solicita una firma de un documento xml, odf o msoffice para un usuario 

        Los valores a suministrar en el parámetro data son:

        * **institution:** uid de la institucion ver code en detalles de institución,
        * **notification_url:** URL para la notificación (debe estar inscrita) o N/D si marca falso en not_webapp,
        * **document:** Archivo en base64, 
        * **format:** tipo de archivo (xml_cofirma, xml_contrafirma, odf, msoffice, pdf), 
        * **algorithm_hash:** algoritmo usado para calcular hash, 
        * **document_hash:** hash del documento,
        * **request_datetime:** Hora de petición en formato '%Y-%m-%d %H:%M:%S', osea  '2006-10-25 14:30:59'
        * **reason:**  Razón de firma PDF (obligatorio solo en PDF)
        * **place:**  Lugar de firma en PDF (obligatorio solo en PDF)
        * **eta:** (Opcional) fecha en formato '%Y-%m-%d %H:%M:%S' a la que se desea firmar, útil en operaciones masivas
        Data es un diccionario, osea un objeto de tipo clave -> valor

        Los valores devueltos son: 

        * **expiration_datetime:** hora final de validez
        * **id_transaction:** Id de trasnacción en el FVA del BCCR
        * **signed_document:** Normalmente None, es un campo para almacenar el documento, pero no se garantiza que venga el documento firmado
        * **status:** Código de error de la transacción
        * **status_text** Descripción para humanos del código de error
        * **received_notification** True si el documento ha sido firmado, False si está en cola
        * **hash_docsigned:**  Normalmente Null,  Base64 hash del documento firmado si el documento existe
        * **hash_id_docsigned:** 0- no se ha firmado 1- Sha256, 2- Sha384, 3- Sha512
        """

        ip = get_ip(request)
        if settings.LOGGING_ENCRYPTED_DATA:
            logger.debug({'message': "Stamp: Create Institution", 'data':
                {'ip': ip, 'data': request.data}, 'location': __file__}, sector=self.log_sector)
        logger.info({'message': 'Stamp: Create Institution ',
                    'data': get_log_institution_information(request), 'location': __file__}, sector=self.log_sector)
        self.time_messages['operation_type'] = "Stamper"
        response = self._create(request, *args, **kwargs)
        metric = self.save_request_metrics(request)
        if hasattr(self, 'serializer'):
            self.serializer.adr.system_metrics = metric
            self.serializer.adr.save()
            self.serializer.call_bccr()
        return response

    @action(detail=True, methods=['post'])
    def institution_show(self, request, *args, **kwargs):
        """
        ::

          POST /stamp/{id_transaction}/institution_show/

        Verifica la firma con sello electrónico dado un código y si respectiva identificación

        Los valores a suministrar en el parámetro data son:

        * **institution:** uid de la institucion ver code en detalles de institución,
        * **notification_url:** URL para la notificación (debe estar inscrita) o N/D si marca falso en not_webapp,
        * **request_datetime:** Hora de petición en formato '%Y-%m-%d %H:%M:%S', osea  '2006-10-25 14:30:59'

        Data es un diccionario, osea un objeto de tipo clave -> valor

        **id_transaction** Corresponde al id del Modelo ya que el BCCR no tiene transaction id

        Los valores devueltos son: 

        * **expiration_datetime:** hora final de validez
        * **request_datetime:** Hora de recepción de la solicitud
        * **id_transaction:** Id de trasnacción en el FVA del BCCR
        * **signed_document:** Normalmente None, es un campo para almacenar el documento, pero no se garantiza que venga el documento firmado
        * **status:** Código de error de la transacción
        * **status_text** Descripción para humanos del código de error
        * **code:** Código para mostrar al usuario
        * **received_notification** True si la autenticación ha sido procesada, False si está esperando al usuario
        * **hash_docsigned:**  Normalmente Null,  Base64 hash del documento firmado si el documento existe
        * **hash_id_docsigned:** 0- no se ha firmado 1- Sha256, 2- Sha384, 3- Sha512
        """
        ip = get_ip(request)
        if settings.LOGGING_ENCRYPTED_DATA:
            logger.debug({'message': 'Show Institution', 'data':
                {'ip':ip, 'data': request.data}, 'location': __file__}, sector=self.log_sector)
        logger.info({'message': 'Show Institution', 'data':
                    get_log_institution_information(request), 'location': __file__},
                    sector=self.log_sector)
        return self.show(request, *args, **kwargs)

    @action(detail=True, methods=['post'])
    def institution_delete(self, request, *args, **kwargs):
        """
        ::

          POST /stamp/{id_transaction}/institution_delete/

        Elimina una petición de firma dado un código de transacción del BCCR

        Los valores a suministrar en el parámetro data son:

        * **institution:** uid de la institucion ver code en detalles de institución,
        * **notification_url:** URL para la notificación (debe estar inscrita) o N/D si marca falso en not_webapp,   
        * **request_datetime:** Hora de petición en formato '%Y-%m-%d %H:%M:%S', osea  '2006-10-25 14:30:59'

        Data es un diccionario, osea un objeto de tipo clave -> valor

        **id_transaction** Corresponde al id del Modelo

        Los valores devueltos son: 

        * **result** True/False si se eliminó la petición o no

        """
        ip = get_ip(request)
        if settings.LOGGING_ENCRYPTED_DATA:
            logger.debug({'message':'Stamp: Delete Institution', 'data':
                {'ip':ip, 'data':request.data}, 'location': __file__}, sector=self.log_sector)
        logger.info({'message': 'Stamp: Delete Institution', 'data':
                    get_log_institution_information(request), 'location': __file__}, sector=self.log_sector)
        return self.delete(request, *args, **kwargs)

    def get_error_response(self, serializer):
        error_code = 2
        if serializer.status_code != -1:
            error_code = serializer.status_code

        if 'data_internal' in serializer.errors :
            for x in serializer.errors['data_internal']:
                if 'reason' in x:
                    error_code = 8
                    break
                elif 'place' in x:
                    error_code = 11
                    break

        dev = {
            'status': error_code,
            'status_text': get_text_representation(
                pyfva.constants.ERRORES_AL_SOLICITAR_SELLO, error_code),

            'id_transaction': 0,
            'request_datetime': timezone.now(),
            'signed_document': None,
            'expiration_datetime': None,
            'received_notification': False,
            'error_info': serializer._errors
        }
        logger.debug({'message':'Stamp: ERROR Institution ', 'data':
                     dev, 'location': __file__}, sector=self.log_sector)
        return Response(self.get_encrypted_response(dev, serializer))
