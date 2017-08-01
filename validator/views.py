from rest_framework import mixins, viewsets
from rest_framework import status
from rest_framework.response import Response
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
# Create your views here.


class ValidateResquestViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = ValidateCertificate_Request_Serializer
    queryset = ValidateCertificateRequest.objects.all()
    response_serializer_class = ValidateCertificateRequest_Response_Serializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        adr = self.response_serializer_class(serializer.adr)
        # adr.is_valid(raise_exception=False)
        return Response(adr.data, status=status.HTTP_201_CREATED, headers=headers)


class ValidateCertificateRequestViewSet(ValidateResquestViewSet):
    serializer_class = ValidateCertificate_Request_Serializer
    queryset = ValidateCertificateRequest.objects.all()
    response_serializer_class = ValidateCertificateRequest_Response_Serializer


class ValidateDocumentRequestViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = ValidateDocument_Request_Serializer
    queryset = ValidateDocumentRequest.objects.all()
    response_serializer_class = ValidateDocumentRequest_Response_Serializer


class ValidateInstitutionViewSet(viewsets.GenericViewSet):
    serializer_class = ValidateCertificate_Request_Serializer
    queryset = ValidateCertificateRequest.objects.all()

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
        return ValidateCertificateRequestViewSet.as_view({'post': 'create'})(request, *args, **kwargs)

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
        return ValidateDocumentRequestViewSet.as_view({'post': 'create'})(request, *args, **kwargs)


class ValidatePersonCertificateRequestViewSet(ValidateResquestViewSet):
    serializer_class = ValidatePersonCertificate_Request_Serializer
    queryset = ValidatePersonCertificateRequest.objects.all()
    response_serializer_class = ValidatePersonCertificateRequest_Response_Serializer


class ValidatePersonDocumentRequestViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = ValidatePersonDocument_Request_Serializer
    queryset = ValidatePersonDocumentRequest.objects.all()
    response_serializer_class = ValidatePersonDocumentRequest_Response_Serializer


class ValidatePersonViewSet(viewsets.GenericViewSet):
    serializer_class = ValidatePersonCertificate_Request_Serializer
    queryset = ValidatePersonCertificateRequest.objects.all()

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
        return ValidatePersonCertificateRequestViewSet.as_view({'post': 'create'})(request, *args, **kwargs)

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
        return ValidatePersonDocumentRequestViewSet.as_view({'post': 'create'})(request, *args, **kwargs)
