# encoding: utf-8


'''
Created on 18/7/2017

@author: luisza
'''


# Create your views here.

from __future__ import unicode_literals

import os

from cruds_adminlte.crud import UserCRUDView
from cruds_adminlte.inline_crud import InlineAjaxCRUD
from django.conf import settings
from django.http.response import HttpResponseRedirect

from .models import Institution, NotificationURL
from corebase.ca_management import gen_cert
from rest_framework.settings import api_settings
from rest_framework import status, mixins, viewsets
from rest_framework.response import Response

# PERSON
from corebase.models import PersonLogin
from corebase.serializer import PersonLoginSerializer,\
    PersonLoginResponseSerializer
from corebase.rsa import get_reponse_person_data_encrypted

from pyfva.constants import get_text_representation
import logging
from corebase.rsa import get_reponse_institution_data_encrypted
logger = logging.getLogger('dfva')

class NotificationURLAjaxCRUD(InlineAjaxCRUD):
    model = NotificationURL
    base_model = Institution
    inline_field = 'institution'
    fields = ['description', 'url', 'not_webapp']
    title = "Direcciones de notificación"


class InstitutionCRUD(UserCRUDView):
    model = Institution
    check_login = True
    check_perms = True
    fields = ['name', 'domain', 'institution_unit', 'active']
    list_fields = ['name', 'domain', 'institution_unit', 'active']
    display_fields = ['name', 'code',  'domain', 'institution_unit', 'active', 'private_key', 'server_public_key',
                      'public_certificate']

    inlines = [NotificationURLAjaxCRUD]

    def get_create_view(self):
        CView = UserCRUDView.get_create_view(self)

        class CreateView(CView):

            def form_valid(self, form):
                self.object = form.save(commit=False)
                self.object = gen_cert(self.object.domain, self.object,
                                       os.path.join(
                                           settings.CA_PATH, "ca_cert.pem"),
                                       os.path.join(settings.CA_PATH, "ca_key.pem"))
                self.object.user = self.request.user
                self.object.save()
                return HttpResponseRedirect(self.get_success_url())

        return CreateView


class ViewSetBase:

    def get_encrypted_response(self, data, serializer):
        dev = {}
        if "institution" in serializer.fields:
            dev = get_reponse_institution_data_encrypted(
                data, serializer.institution,
                algorithm=serializer.data.get('algorithm', "sha512"))
        else:  # person
            dev = get_reponse_person_data_encrypted(
                data,
                serializer.person.authenticate_certificate if hasattr(
                    serializer, 'person') else None,
                algorithm=serializer.data.get('algorithm', "sha512"))

        return dev

    def get_success_headers(self, data):
        try:
            return {'Location': data[api_settings.URL_FIELD_NAME]}
        except (TypeError, KeyError):
            return {}

    def _create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=False):
            serializer.save()
            headers = self.get_success_headers(serializer.data)
            adr = self.response_class(serializer.adr)
            logger.debug('Data create Response: %r' % (serializer.adr,))
            # adr.is_valid(raise_exception=False)
            logger.info('Response create ok %s' %
                        (serializer.data['data_hash']))

            return Response(self.get_encrypted_response(adr.data, serializer), status=status.HTTP_201_CREATED, headers=headers)
        logger.info('Response create ERROR %s' %
                    (serializer.data['data_hash'] if 'data_hash' in serializer.data else '',))
        return self.get_error_response(serializer)

    def show(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.check_code(kwargs['pk'], raise_exception=False):
            headers = self.get_success_headers(serializer.data)
            adr = self.response_class(serializer.adr)
            logger.debug('Data create Response: %r' % (serializer.adr,))
            logger.info('Response show ok %s' %
                        (serializer.data['data_hash'], ))
            # adr.is_valid(raise_exception=False)
            return Response(self.get_encrypted_response(adr.data, serializer),
                            status=status.HTTP_201_CREATED, headers=headers)

        logger.info('Response show ERROR %s' %
                    (serializer.data['data_hash'] if 'data_hash' in serializer.data else '',))
        return self.get_error_response(serializer)

    def get_error_response(self, serializer):
        dev = {"error_info": serializer._errors,
               'code': 'N/D',
               'status': 2,
               'status_text': get_text_representation(
                   self.DEFAULT_ERROR,  2),
               'id_transaction': 0
               }
        logger.debug('ViewSetBase Error %r' %
                     (dev, ))
        return Response(self.get_encrypted_response(dev, serializer))


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
        return Response(dev, status=status.HTTP_201_CREATED, headers=headers)
