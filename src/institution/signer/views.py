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
from institution.signer.serializer import Sign_Request_Serializer,\
    Sign_Response_Serializer
from institution.models import SignRequest
from corebase.logging import get_ip, get_log_institution_information
from pyfva.constants import get_text_representation
import pyfva
import logging
from django.conf import settings
from rest_framework.decorators import action

from corebase import logger


class SignRequestViewSet(ViewSetBase,
                         viewsets.GenericViewSet):

    serializer_class = Sign_Request_Serializer
    queryset = SignRequest.objects.all()
    response_class = Sign_Response_Serializer
    log_sector = 'sign'

    @action(detail=False, methods=['post'])
    def institution(self, request, *args, **kwargs):
        """
        ::

          POST /sign/institution/

        Solicita una firma de un documento xml, odf o msoffice para un usuario 

        Los valores a suministrar en el parámetro data son:

        * **institution:** uid de la institucion ver code en detalles de institución,
        * **notification_url:** URL para la notificación (debe estar inscrita) o N/D si marca falso en not_webapp,
        * **document:** Archivo en base64, 
        * **format:** tipo de archivo (xml_cofirma, xml_contrafirma, odf, msoffice, pdf), 
        * **algorithm_hash:** algoritmo usado para calcular hash, 
        * **document_hash:** hash del documento,
        * **resumen:** Información de ayuda acerca del documento,      
        * **identification:** Identificación de la persona a autenticar,
        * **request_datetime:** Hora de petición en formato '%Y-%m-%d %H:%M:%S', osea  '2006-10-25 14:30:59'
        * **reason:**  Razón de firma PDF (obligatorio solo en PDF)
        * **place:**  Lugar de firma en PDF (obligatorio solo en PDF)

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
        * **resume:** Resumen de la transacción.
        * **hash_docsigned:**  Normalmente Null,  Base64 hash del documento firmado si el documento existe
        * **hash_id_docsigned:** 0- no se ha firmado 1- Sha256, 2- Sha384, 3- Sha512
        """

        ip = get_ip(request)
        if settings.LOGGING_ENCRYPTED_DATA:
            logger.debug({'message': "Sign: Create Institution", 'data':
                {'ip': ip, 'data': request.data}, 'location': __file__}, sector=self.log_sector)
        logger.info({'message': 'Sign: Create Institution ',
                    'data': get_log_institution_information(request), 'location': __file__}, sector=self.log_sector)
        self.time_messages['operation_type'] = "Signer"
        response = self._create(request, *args, **kwargs)
        self.save_request_metrics(request)
        return  response

    @action(detail=True, methods=['post'])
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
        * **resume:** Resumen de la transacción.
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
        if settings.LOGGING_ENCRYPTED_DATA:
            logger.debug({'message':'Sign: Delete Institution', 'data':
                {'ip':ip, 'data':request.data}, 'location': __file__}, sector=self.log_sector)
        logger.info({'message': 'Sign: Delete Institution', 'data':
                    get_log_institution_information(request), 'location': __file__}, sector=self.log_sector)
        return self.delete(request, *args, **kwargs)

    def get_error_response(self, serializer):
        error_code = 2
        if serializer.status_code != -1:
            error_code = serializer.status_code

        if 'data_internal' in serializer.errors :
            for x in serializer.errors['data_internal']:
                if 'identification' in x:
                    error_code = 10
                    break
                elif 'reason' in x:
                    error_code = 8
                    break
                elif 'place' in x:
                    error_code = 11
                    break
                elif 'resumen' in x:
                    error_code = 7
                    break
        dev = {
            'code': 'N/D',
            'status': error_code,
            'status_text': get_text_representation(
                pyfva.constants.ERRORES_AL_SOLICITAR_FIRMA, error_code),
            'identification': 'N/D',
            'id_transaction': 0,
            'request_datetime': timezone.now(),
            'sign_document': None,
            'expiration_datetime': None,
            'received_notification': False,
            'error_info': serializer._errors
        }
        logger.debug({'message':'Sign: ERROR Institution ', 'data':
                     dev, 'location': __file__}, sector=self.log_sector)
        return Response(self.get_encrypted_response(dev, serializer))
