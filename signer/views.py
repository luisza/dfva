
from rest_framework import viewsets
from rest_framework.response import Response

from signer.models import SignRequest
from signer.serializer import Sign_Request_Serializer, Sign_Response_Serializer
from rest_framework.decorators import detail_route, list_route
from django.utils import timezone
from corebase.views import ViewSetBase

# person
from signer.models import SignPersonRequest
from signer.serializer import Sign_Person_Request_Serializer, Sign_Person_Response_Serializer


class SignRequestViewSet(ViewSetBase,
                         viewsets.GenericViewSet):
    """Solicita una firma de un documento xml, odf o msoffice para un usuario 

    Los valores a suministrar en el parámetro data son:

    * **institution:** uid de la institucion ver code en detalles de institución,
    * **notification_url:** URL para la notificación (debe estar inscrita) o N/D si marca falso en not_webapp,
    * **document:** Archivo en base64, 
    * **format:** tipo de archivo (xml, odf, msoffice), 
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
    * **identification:** Identificador del suscriptor
    * **code:** Código para mostrar al usuario
    * **received_notification** True si la autenticación ha sido procesada, False si está esperando al usuario

    """

    serializer_class = Sign_Request_Serializer
    queryset = SignRequest.objects.all()
    response_class = Sign_Response_Serializer

    @list_route(methods=['post'])
    def institution(self, request, *args, **kwargs):
        return self._create(request, *args, **kwargs)

    @detail_route(methods=['post'])
    def institution_show(self, request, *args, **kwargs):
        """Verifica la firma dado un código y si respectiva identificación

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
        * **sign_document:** Normalmente None, es un campo para almacenar el documento, pero no se garantiza que venga el documento firmado
        * **status:** Código de error de la transacción
        * **identification:** Identificador del suscriptor
        * **code:** Código para mostrar al usuario
        * **received_notification** True si la autenticación ha sido procesada, False si está esperando al usuario

        """
        return self.show(request, *args, **kwargs)

    def get_error_response(self):
        return Response({
            'code': 'N/D',
            'status': 2,
            'identification': 'N/D',
            'id_transaction': 0,
            'request_datetime': timezone.now(),
            'sign_document': None,
            'expiration_datetime': None,
            'received_notification': False
        })


class SignPersonRequestViewSet(ViewSetBase,
                               viewsets.GenericViewSet):
    """Solicita una firma de un documento xml, odf o msoffice para un usuario 

    Los valores a suministrar en el parámetro data son:

    * **person:** identificación de la persona solicitante de firma,
    * **notification_url:** URL para la notificación (debe estar inscrita) o N/D si marca falso en not_webapp,
    * **document:** Archivo en base64, 
    * **format:** tipo de archivo (xml, odf, msoffice), 
    * **algorithm_hash:** algoritmo usado para calcular hash, 
    * **document_hash:** hash del documento,
    * **resumen:** Información de ayuda acerca del documento,      
    * **identification:** Identificación de la persona a firmar,
    * **request_datetime:** Hora de petición en formato '%Y-%m-%d %H:%M:%S', osea  '2006-10-25 14:30:59'

    Data es un diccionario, osea un objeto de tipo clave -> valor

    Los valores devueltos son: 

    * **expiration_datetime:** hora final de validez
    * **request_datetime:** Hora de recepción de la solicitud
    * **id_transaction:** Id de trasnacción en el FVA del BCCR
    * **sign_document:** Normalmente None, es un campo para almacenar el documento, pero no se garantiza que venga el documento firmado
    * **status:** Código de error de la transacción
    * **identification:** Identificador del suscriptor
    * **code:** Código para mostrar al usuario
    * **received_notification** True si la autenticación ha sido procesada, False si está esperando al usuario

    """

    serializer_class = Sign_Person_Request_Serializer
    queryset = SignPersonRequest.objects.all()
    response_class = Sign_Person_Response_Serializer

    @list_route(methods=['post'])
    def person(self, request, *args, **kwargs):
        return self._create(request, *args, **kwargs)

    @detail_route(methods=['post'])
    def person_show(self, request, *args, **kwargs):
        """Verifica la firma dado un código y su respectiva identificación

        Los valores a suministrar en el parámetro data son:

        * **person:** identificación de la persona solicitante de firma,
        * **identification:** Identificación de la persona a autenticar,
        * **request_datetime:** Hora de petición en formato '%Y-%m-%d %H:%M:%S', osea  '2006-10-25 14:30:59'

        Data es un diccionario, osea un objeto de tipo clave -> valor

        Los valores devueltos son: 

        * **expiration_datetime:** hora final de validez
        * **request_datetime:** Hora de recepción de la solicitud
        * **id_transaction:** Id de trasnacción en el FVA del BCCR
        * **sign_document:** Normalmente None, es un campo para almacenar el documento, pero no se garantiza que venga el documento firmado
        * **status:** Código de error de la transacción
        * **identification:** Identificador del suscriptor
        * **code:** Código para mostrar al usuario
        * **received_notification** True si la autenticación ha sido procesada, False si está esperando al usuario

        """
        return self.show(request, *args, **kwargs)

    def get_error_response(self):
        return Response({
            'code': 'N/D',
            'status': 2,
            'identification': 'N/D',
            'id_transaction': 0,
            'request_datetime': timezone.now(),
            'sign_document': None,
            'expiration_datetime': None,
            'received_notification': False
        })
