from rest_framework import status, mixins, viewsets
from rest_framework.response import Response
import logging
from person.models import PersonLogin
from person.serializer import PersonLoginSerializer,\
    PersonLoginResponseSerializer
from django.conf import settings


logger = logging.getLogger(settings.DEFAULT_LOGGER_NAME)


class PersonLoginView(mixins.CreateModelMixin,
                      viewsets.GenericViewSet):

    queryset = PersonLogin.objects.all()
    serializer_class = PersonLoginSerializer
    response_class = PersonLoginResponseSerializer

    def create(self, request, *args, **kwargs):
        """
        .. note:: Esta vista no está encriptada.

        ::

          POST /login/

        Permite a una persona autenticarse en DFVA, un token de sección es retornado
        y deberá ser usuado para encriptar la comunicación.

        Los valores a suministrar son:

        * **data_hash:** Suma hash de datos de tamaño máximo 130 caracteres, usando el algoritmo especificado 
        * **algorithm:** Algoritmo con que se construye data_hash, debe ser alguno de los siguientes: sha256, sha384, sha512
        * **public_certificate:** Certificado de autenticación del dispositivo pkcs11
        * **person:** Identificación de la persona,
        * **code**: Identificación de la persona firmada con la llave privada del certificado de autenticación.

        Los valores devueltos son: 

        * **identification**:  Identificación del suscriptor
        * **token**: Token de sección para encriptar atributo data posteriormente
        * **expiration_datetime_token**:  Hora máxima para usar el token 
        * **last_error_code**:  Código de estado de la transacción
        * **error_text**: Descripción de los errores encontrados       

        """

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=False):
            data = serializer.save()
            headers = self.get_success_headers(data.data)
            logger.debug('Data login Response: %r' % (data.data,))
            logger.info('Response login ok')
            return Response(data.data, status=status.HTTP_201_CREATED, headers=headers)

        dev = {
            'identification': 'N/D',
            'token': None,
            'expiration_datetime_token': None,
            'last_error_code': 3,
            'error_text': repr(serializer._errors)
        }
        logger.info('Response login ERROR %r' % (serializer._errors, ))
        logger.debug('Data login Response error: %r' % (dev,))
        return Response(dev, status=status.HTTP_201_CREATED)
