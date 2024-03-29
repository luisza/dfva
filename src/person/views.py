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
import random

from django import forms
from rest_framework import status, mixins, viewsets
from rest_framework.response import Response
import logging
from person.models import PersonLogin
from person.serializer import PersonLoginSerializer, \
    PersonLoginResponseSerializer, OperandLogin
from django.conf import settings


logger = logging.getLogger(settings.DEFAULT_LOGGER_NAME)


class AutenticationLoginForm(forms.Form):
    serial = forms.CharField(required=True, max_length=64)
    identification = forms.CharField(required=True, max_length=17)


class PersonLoginView(mixins.CreateModelMixin, mixins.ListModelMixin,
                      viewsets.GenericViewSet):

    queryset = PersonLogin.objects.all()
    serializer_class = PersonLoginSerializer
    response_class = PersonLoginResponseSerializer

    def create(self, request, *args, **kwargs):
        """
        Autentica el usuario usando una prueba de verdad.

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
        * **transaction_id**: Id de transacción usado para determinar la operación.

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

    def list(self, request, *args, **kwargs):
        """
        Gestiona la operación de verdad, para la generación de token a firmar.
        En el flujo se solicita a esta vista 2 operadores y una función de operación, luego el cliente calcula el
        resultado y lo envía firmado a la vísta vía POST, SIFVA valida el resultado y lo compara con lo enviado, si
        ambos son iguales entonces autentica al usuario.

        ::

         GET /login/     
         
        Parámetros GET

        * **serial:** Serial de la tarjeta con la cual autenticarse.
        * **person:** Identificación de la persona

        Response:

        * **transaction_id:** ID del objeto de autenticación.
        * **operatorA:** Operadorador izquierdo
        * **operand:** Operadorador
        * **operatorB:** Operadorador derecho
            
        """

        form = AutenticationLoginForm(request.data or request.GET)
        if form.is_valid():

            instance, created = PersonLogin.objects.get_or_create(person=form.cleaned_data['identification'],
                                                                  serial=form.cleaned_data)
            instance.operatorA = random.randint(1000, 2**30)
            instance.operatorB = random.randint(1000, 2**30)
            instance.operand = OperandLogin.get_operand()
            instance.algorithm = 'sha256'
            instance.save()
            dev = {
                'transaction_id': instance.pk,
                'operatorA': instance.operatorA,
                'operatorB': instance.operatorB,
                'operand': instance.operand,
                'algorithm': instance.algorithm
            }
            return Response(dev, status=status.HTTP_200_OK)
        return Response({}, status=status.HTTP_401_UNAUTHORIZED)