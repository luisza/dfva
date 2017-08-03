from validator.serializer import ValidateCertificate_Request_Serializer,\
    ValidateDocument_Request_Serializer,\
    ValidateCertificateRequest_Response_Serializer,\
    ValidateDocumentRequest_Response_Serializer,\
    ValidatePersonCertificate_Request_Serializer,\
    ValidatePersonDocument_Request_Serializer,\
    ValidatePersonCertificateRequest_Response_Serializer,\
    ValidatePersonDocumentRequest_Response_Serializer
from validator.models import ValidateCertificateRequest,\
    ValidateDocumentRequest, ValidatePersonCertificateRequest,\
    ValidatePersonDocumentRequest
from rest_framework.decorators import list_route
from corebase.views import ViewSetBase
from rest_framework import viewsets
# Create your views here.


class ValidateInstitutionViewSet(ViewSetBase, viewsets.GenericViewSet):
    serializer_class = ValidateCertificate_Request_Serializer
    queryset = ValidateCertificateRequest.objects.all()
    response_class = ValidateCertificateRequest_Response_Serializer

    @list_route(methods=['post'])
    def institution_certificate(self, request, *args, **kwargs):
        """Solicita una de un certificado de autenticación para un usuario 

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
        * **codigo_de_error:**  Códigos de error del certificado, si existen
        * **nombre_completo:**  Nombre completo del suscriptor
        * **inicio_vigencia:**  Inicio de la vigencia del certificado
        * **fin_vigencia:**  Fin de la vigencia del certificado
        * **fue_exitosa:**  Si la verificación del certificado fue exitosa

        **Nota:**  Si la validación del certificado no fue exitosa, entonces los campos de identificación, nombre_completo, inicio_vigencia,
        fin_vigencia deben ignorase o son nulos.

        """
        return self._create(request, *args, **kwargs)

    @list_route(methods=['post'])
    def institution_document(self, request, *args, **kwargs):
        """Solicita una verificación de firma  de un documento xml  

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
        * **advertencias:** Lista de advertencias
        * **errores:** Lista de errores encontrados en el documento del tipo [ {'codigo': 'codigo','descripcion': 'descripción'}, ... ]
        * **firmantes:** Lista con la información de los firmantes [ {'cedula': '08-8888-8888', 'nombre_completo': 'nombre del suscriptor', 'fecha_de_firma': timezone.now()}, ... ]
        * **fue_exitosa:**  Si la verificación del certificado fue exitosa

        **Nota:**  Si la validación del documento no fue exitosa, entonces los campos de firmantes deben ignorase o son nulos.

        """

        self.serializer_class = ValidateDocument_Request_Serializer
        self.queryset = ValidateDocumentRequest.objects.all()
        self.response_class = ValidateDocumentRequest_Response_Serializer
        return self._create(request, *args, **kwargs)


class ValidatePersonViewSet(ViewSetBase, viewsets.GenericViewSet):
    serializer_class = ValidatePersonCertificate_Request_Serializer
    queryset = ValidatePersonCertificateRequest.objects.all()
    response_class = ValidatePersonCertificateRequest_Response_Serializer

    @list_route(methods=['post'])
    def person_certificate(self, request, *args, **kwargs):
        """Solicita una de un certificado de autenticación para un usuario 

        Los valores a suministrar en el parámetro data son:

        * **person:** Identificación de la persona validante,
        * **notification_url:** URL para la notificación (debe estar inscrita) o N/D si marca falso en not_webapp,
        * **document:** Archivo en base64 del certificado, 
        * **request_datetime:** Hora de petición en formato '%Y-%m-%d %H:%M:%S', osea  '2006-10-25 14:30:59'

        Data es un diccionario, osea un objeto de tipo clave -> valor

        Los valores devueltos son: 

        * **identification:**  Identificación del suscriptor
        * **request_datetime:**  Hora de recepción de la solicitud
        * **code:** Código de identificación de la transacción (no es el mismo que el que se muestra en al usuario en firma)
        * **status:** Estado de la solicitud
        * **codigo_de_error:**  Códigos de error del certificado, si existen
        * **nombre_completo:**  Nombre completo del suscriptor
        * **inicio_vigencia:**  Inicio de la vigencia del certificado
        * **fin_vigencia:**  Fin de la vigencia del certificado
        * **fue_exitosa:**  Si la verificación del certificado fue exitosa

        **Nota:**  Si la validación del certificado no fue exitosa, entonces los campos de identificación, nombre_completo, inicio_vigencia,
        fin_vigencia deben ignorase o son nulos.

        """
        return self._create(request, *args, **kwargs)

    @list_route(methods=['post'])
    def person_document(self, request, *args, **kwargs):
        """Solicita una verificación de firma  de un documento xml  

        Los valores a suministrar en el parámetro data son:

        * **person:** Identificación de la persona validante,
        * **notification_url:** URL para la notificación (debe estar inscrita) o N/D si marca falso en not_webapp,
        * **document:** Archivo en base64 del certificado, 
        * **request_datetime:** Hora de petición en formato '%Y-%m-%d %H:%M:%S', osea  '2006-10-25 14:30:59'

        Data es un diccionario, osea un objeto de tipo clave -> valor

        Los valores devueltos son: 

        * **identification:**  Identificación del suscriptor
        * **request_datetime:**  Hora de recepción de la solicitud
        * **code:** Código de identificación de la transacción (no es el mismo que el que se muestra en al usuario en firma)
        * **status:** Estado de la solicitud
        * **advertencias:** Lista de advertencias
        * **errores:** Lista de errores encontrados en el documento del tipo [ {'codigo': 'codigo','descripcion': 'descripción'}, ... ]
        * **firmantes:** Lista con la información de los firmantes [ {'cedula': '08-8888-8888', 'nombre_completo': 'nombre del suscriptor', 'fecha_de_firma': timezone.now()}, ... ]
        * **fue_exitosa:**  Si la verificación del certificado fue exitosa

        **Nota:**  Si la validación del documento no fue exitosa, entonces los campos de firmantes deben ignorase o son nulos.

        """
        self.serializer_class = ValidatePersonDocument_Request_Serializer
        self.queryset = ValidatePersonDocumentRequest.objects.all()
        self.response_class = ValidatePersonDocumentRequest_Response_Serializer

        return self._create(request, *args, **kwargs)
