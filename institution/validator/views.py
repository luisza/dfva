'''
Created on 13 sep. 2017

@author: luisza
'''
import logging
from corebase.views import ViewSetBase, BaseSuscriptor
from rest_framework import viewsets
from institution.validator.serializer import ValidateCertificate_Request_Serializer,\
    ValidateCertificateRequest_Response_Serializer,\
    ValidateDocument_Request_Serializer,\
    ValidateDocumentRequest_Response_Serializer,\
    SuscriptorInstitution_Serializer
from institution.models import ValidateCertificateRequest,\
    ValidateDocumentRequest
from pyfva.constants import ERRORES_VALIDA_CERTIFICADO, ERRORES_VALIDA_DOCUMENTO
from rest_framework.decorators import list_route
from corebase.logging import get_ip, get_log_institution_information

logger = logging.getLogger('dfva')

class ValidateInstitutionViewSet(ViewSetBase, viewsets.GenericViewSet):
    serializer_class = ValidateCertificate_Request_Serializer
    queryset = ValidateCertificateRequest.objects.all()
    response_class = ValidateCertificateRequest_Response_Serializer
    DEFAULT_ERROR = ERRORES_VALIDA_CERTIFICADO

    @list_route(methods=['post'])
    def institution_certificate(self, request, *args, **kwargs):
        """
        ::

          POST /validate/institution_certificate/

        Solicita una de un certificado de autenticación para un usuario 

        Los valores a suministrar en el parámetro data son:

        * **institution:** uid de la institucion ver code en detalles de institución,
        * **notification_url:** URL para la notificación (debe estar inscrita) o N/D si marca falso en not_webapp,
        * **document:** Archivo en base64 del certificado, 
        * **request_datetime:** Hora de petición en formato '%Y-%m-%d %H:%M:%S', osea  '2006-10-25 14:30:59'

        Data es un diccionario, osea un objeto de tipo clave -> valor

        Los valores devueltos son: 

        * **identification:**  Identificación del suscriptor
        * **request_datetime:**  Hora de recepción de la solicitud
        * **code:** Código de identificación de la transacción (no es el mismo que el que se muestra en al usuario en firma)
        * **status:** Estado de la solicitud
        * **status_text:**  Descripción en texto del estado
        * **nombre_completo:**  Nombre completo del suscriptor
        * **inicio_vigencia:**  Inicio de la vigencia del certificado
        * **fin_vigencia:**  Fin de la vigencia del certificado
        * **fue_exitosa:**  Si la verificación del certificado fue exitosa

        **Nota:**  Si la validación del certificado no fue exitosa, entonces los campos de identificación, nombre_completo, inicio_vigencia,
        fin_vigencia deben ignorase o son nulos.

        """
        ip = get_ip(request)
        logger.debug('Validator: Certificate Institution %s %r' %
                     (ip, request.data))
        logger.info('Validator: Certificate Institution %s %s %s %s' %
                    get_log_institution_information(request))
        self.DEFAULT_ERROR = ERRORES_VALIDA_CERTIFICADO
        return self._create(request, *args, **kwargs)

    @list_route(methods=['post'])
    def institution_document(self, request, *args, **kwargs):
        """
        ::

          POST /validate/institution_document/  
        
        Solicita una verificación de firma  de un documento xml  

        Los valores a suministrar en el parámetro data son:

        * **institution:** uid de la institucion ver code en detalles de institución,
        * **notification_url:** URL para la notificación (debe estar inscrita) o N/D si marca falso en not_webapp,
        * **document:** Archivo en base64 del certificado, 
        * **request_datetime:** Hora de petición en formato '%Y-%m-%d %H:%M:%S', osea  '2006-10-25 14:30:59'

        Data es un diccionario, osea un objeto de tipo clave -> valor

        Los valores devueltos son: 

        * **identification:**  Identificación del suscriptor
        * **request_datetime:**  Hora de recepción de la solicitud
        * **code:** Código de identificación de la transacción (no es el mismo que el que se muestra en al usuario en firma)
        * **status:** Estado de la solicitud
        * **status_text:**  Descripción en texto del estado
        * **advertencias:** Lista de advertencias
        * **errores:** Lista de errores encontrados en el documento del tipo [ {'codigo': 'codigo','descripcion': 'descripción'}, ... ]
        * **firmantes:** Lista con la información de los firmantes [ {'cedula': '08-8888-8888', 'nombre_completo': 'nombre del suscriptor', 'fecha_de_firma': timezone.now()}, ... ]
        * **fue_exitosa:**  Si la verificación del certificado fue exitosa

        **Nota:**  Si la validación del documento no fue exitosa, entonces los campos de firmantes deben ignorase o son nulos.

        """

        ip = get_ip(request)
        logger.debug('Validator: Document Institution %s %r' %
                     (ip, request.data))
        logger.info('Validator: Document Institution %s %s %s %s' %
                    get_log_institution_information(request))
        self.serializer_class = ValidateDocument_Request_Serializer
        self.queryset = ValidateDocumentRequest.objects.all()
        self.response_class = ValidateDocumentRequest_Response_Serializer
        self.DEFAULT_ERROR = ERRORES_VALIDA_DOCUMENTO
        return self._create(request, *args, **kwargs)


class ValidateSubscriptorInstitutionViewSet(BaseSuscriptor, viewsets.GenericViewSet):
    serializer_class = SuscriptorInstitution_Serializer
    queryset = ValidateCertificateRequest.objects.all()


    @list_route(methods=['post'])
    def institution_suscriptor_connected(self, request, *args, **kwargs):
        """
        ::

          POST /validate/institution_suscriptor_connected/
         
        Verifica si una persona está conectada (es contactable por el BCCR).  

        Los valores a suministrar en el parámetro data son:


        * **institution:** uid de la institucion ver code en detalles de institución,
        * **notification_url:** URL para la notificación (debe estar inscrita) o N/D si marca falso en not_webapp,
        * **identification:** Identificación de la persona a buscar, 
        * **request_datetime:** Hora de petición en formato '%Y-%m-%d %H:%M:%S', osea  '2006-10-25 14:30:59'

        Data es un diccionario, osea un objeto de tipo clave -> valor

        **Retorna:** 
            **is_connected:** True si la persona está conectada, false si no lo está
        """
        ip = get_ip(request)
        logger.debug('Connected:  institution %s %r' %
                     (ip, request.data))
        logger.info('Connected:  institution %s %s %s %s' %
                    get_log_institution_information(request))
        return self._create(request,  *args, **kwargs)