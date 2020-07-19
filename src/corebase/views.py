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
@date: 18/7/2017
@author: Universidad de Costa Rica
@maintainer: Luis Zarate Montero
@contact: luis.zarate@solvosoft.com
@license: GPLv3
'''

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response
from rest_framework.settings import api_settings

from authorization_management.forms import RegistationForm, \
    UserConditionsAndTermsForm
from authorization_management.models import UserConditionsAndTerms
from corebase import logger
from corebase.models import System_Request_Metric

from corebase.rsa import get_reponse_institution_data_encrypted
from pyfva.constants import get_text_representation


def check_ok(request):
    """
    This view help to check service status with apps like icinga o nagios
    :param request:
    :return: OK
    """
    return HttpResponse("ok")

def home(request):
    context = {
        'update_profile': False
    }
    user = request.user
    form_post = None
    form = None
    check_form = True
    method = request.method
    if method == 'POST':
        form_post = request.POST
    if user.is_authenticated:

        while check_form:
            check_form = False
            if not user.has_perm('institution.change_institution'):
                context['update_profile'] = True
                if not user.email or not user.first_name or not user.last_name:
                    form = RegistationForm(form_post, instance=user)
                else:
                    ucat = UserConditionsAndTerms.objects.filter(
                        user=user).first()
                    if ucat is None or ucat.signed is False:
                        form = UserConditionsAndTermsForm(
                            form_post,
                            instance=ucat,
                            initial={'text': render_to_string(
                                'terms_conditions/user_terms.html',
                                context={'user': user}
                            )})

            if method == 'POST' and form is not None:
                if form.is_valid():
                    form.save()
                    form = None
                    method = 'GET'
                    check_form = True
                    form_post = None

    if form:
        context['form'] = form
    else:
        context['update_profile'] = False
    return render(request, 'index.html', context)


class ViewSetBase:
    """
    Implementa los métodos que todas las vistas deben implementar para responder en el API
    """
    #: Almacena las métricas de tiempo
    time_messages = {}
    log_sector = 'corebase'

    def get_encrypted_response(self, data, serializer):
        """
        Cuando se debe dar una respuesta, esta se encripta usando la llave pública de la institución

        :param data: Información que se debe encriptar
        :param serializer: Serializador usado para determinar cual es la institución con la que se comunica
        :return: dict - Serializador ya encriptado
        """
        dev = {}
        self.time_messages['start_encryption'] = timezone.now()
        if "institution" in serializer.fields:
            dev = get_reponse_institution_data_encrypted(
                data, serializer.institution,
                algorithm=serializer.data.get('algorithm', "sha512"),
                method=serializer.encrypt_method)
            if hasattr(serializer, 'institution') and serializer.institution:
                self.time_messages['institution'] = serializer.institution
        else:  # person
            dev = data
        self.time_messages['end_encryption'] = timezone.now()
        return dev

    def get_success_headers(self, data):
        """
        Retorna los encabezados http a devolver con ls peticiones
        """
        try:
            return {'Location': data[api_settings.URL_FIELD_NAME]}
        except (TypeError, KeyError):
            return {}

    def _create(self, request, *args, **kwargs):
        """
        Procesa las peticiones de creación (Firma, Autenticación, Validación)

        :return: Http Response con la información serializada e encriptada
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=False):
            serializer.save()
            headers = self.get_success_headers(serializer.data)
            adr = self.response_class(serializer.adr)
            logger.debug({'message':'Data create Response: ', 'data': serializer.adr,
                          'location': __file__}, sector=self.log_sector)
            # adr.is_valid(raise_exception=False)
            logdata = adr.data
            if not settings.LOGGING_ENCRYPTED_DATA:
                logdata = {k: v for k, v in adr.data.items() if k not in ['documento', 'sign_document']}

            logger.info({'message': 'Response create OK', 'data':
                        {'data_hash': serializer.data['data_hash'], 'data':logdata},
                         'location': __file__}, sector=self.log_sector)
            self.time_messages.update(serializer.time_messages)
            return Response(self.get_encrypted_response(adr.data, serializer),
                            status=status.HTTP_201_CREATED, headers=headers)
        logger.info({'messsage': 'Response create ERROR', 'data': {'errors':serializer._errors,
                    'data_hash': serializer.data['data_hash'] if 'data_hash' in
                     serializer.data else '',}, 'location': __file__},
                    sector=self.log_sector)
        self.time_messages.update(serializer.time_messages)
        return self.get_error_response(serializer)

    def show(self, request, *args, **kwargs):
        """
        Implementa las vistas authenticate_show, sign_show, es la vista encargada de verificar el estado
        de la transacción mientras la notificación del BCCR no ha llegado

        :return:  Http Response con la información serializada e encriptada
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.check_code(kwargs['pk'], raise_exception=False):
            headers = self.get_success_headers(serializer.data)
            adr = self.response_class(serializer.adr)
            logger.debug({'message':'Data create Response:', 'data':serializer.adr,
                          'location': __file__}, sector=self.log_sector)
            logdata = adr.data
            if not settings.LOGGING_ENCRYPTED_DATA:
                logdata = {k: v for k, v in adr.data.items() if k not in ['documento', 'sign_document']}
            logger.info({'message': 'Response show OK', 'data':
                {'data_hash': serializer.data['data_hash'], 'data': logdata}, 'location': __file__},
                        sector=self.log_sector)
            # adr.is_valid(raise_exception=False)
            return Response(self.get_encrypted_response(adr.data, serializer),
                            status=status.HTTP_201_CREATED, headers=headers)

        logger.info({'message': 'Response show ERROR', 'data': {'errors': serializer._errors,
                    'data_hash': serializer.data['data_hash'] if 'data_hash' in
                     serializer.data else ''}, 'location': __file__}, sector=self.log_sector)
        return self.get_error_response(serializer)

    def delete(self, request, *args, **kwargs):
        """
        Elimina una transacción del proceso, usada en los métodos authenticate_delete y sign_delete

        :return:  Http Response con la información serializada e encriptada
        """

        dev = False
        serializer = self.get_serializer(data=request.data)
        if serializer.check_code(kwargs['pk'], raise_exception=False):
            if hasattr(serializer.adr, "authenticaterequest"):
                serializer.adr.authenticaterequest.delete()
            if hasattr(serializer.adr, "signrequest"):
                serializer.adr.signrequest.delete()
            serializer.adr.delete()
            dev = True
        logger.info({'message': 'Response delete %s'%( 'OK' if dev else "ERROR"),
                     'data': request.data, 'location': __file__}, sector=self.log_sector)
        response = {'result': dev}
        headers = self.get_success_headers(response)
        return Response(self.get_encrypted_response(response, serializer),
                        status=status.HTTP_201_CREATED, headers=headers)

    def get_error_response(self, serializer):
        """
        Genera un mensaje de error, para cuando no se puede obtener información del BCCR o sucede alguna excepción
        no controlada

        :param serializer: Serializador usado, en caso de errores si gestionables
        :return: Http Response con la información serializada e encriptada
        """
        error_code = 2
        if 'data_internal' in serializer.errors and any(
                ['identification' in x for x in serializer.errors['data_internal'] ]):
            error_code = 10

        if hasattr(serializer, 'error_code'):
            error_code = serializer.error_code

        dev = {"error_info": serializer.errors,
               'code': 'N/D',
               'status': error_code,
               'status_text': get_text_representation(
                   self.DEFAULT_ERROR,  error_code),
               'id_transaction': 0
               }
        logger.debug({'message': 'ViewSetBase Error', 'data': dev, 'location': __file__},
                     sector=self.log_sector)
        self.time_messages['transaction_status'] = dev['status']
        self.time_messages['transaction_status_text'] = dev['status_text']
        self.time_messages['transaction_success'] = settings.DEFAULT_SUCCESS_BCCR == dev['status']
        return Response(self.get_encrypted_response(dev, serializer))

    def save_request_metrics(self, request):
        """
        Almacena las métricas de la transacción antes de responderle al usuario.
        Este método se llama de último al procesar la transacción.

        :return: System_Request_Metric
        """
        self.time_messages['request_size'] = request.META['CONTENT_LENGTH']
        metric = System_Request_Metric(**self.time_messages)
        metric.save()
        return metric


class BaseSuscriptor(ViewSetBase):
    def _create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = {
            'is_connected': serializer.save()
        }

        # adr.is_valid(raise_exception=False)
        return Response(data, status=status.HTTP_200_OK)

    def get_error_response(self, serializer):
        return Response({
            'is_connected':  False,
            'info_error': serializer._errors
        }, status=status.HTTP_200_OK)
