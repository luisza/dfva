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

from __future__ import unicode_literals

import logging
from django.shortcuts import render
from django.template.loader import render_to_string

from authorization_management.forms import RegistationForm, \
    UserConditionsAndTermsForm
from authorization_management.models import UserConditionsAndTerms
from corebase.rsa import (get_reponse_institution_data_encrypted,
                          get_reponse_person_data_encrypted)
from pyfva.constants import get_text_representation
from rest_framework import status
from rest_framework.response import Response
from rest_framework.settings import api_settings
from django.conf import settings

logger = logging.getLogger(settings.DEFAULT_LOGGER_NAME)


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
    if user.is_authenticated():

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

    def get_encrypted_response(self, data, serializer):
        dev = {}
        if "institution" in serializer.fields:
            dev = get_reponse_institution_data_encrypted(
                data, serializer.institution,
                algorithm=serializer.data.get('algorithm', "sha512"),
                method=serializer.encrypt_method)
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

            return Response(self.get_encrypted_response(adr.data, serializer),
                            status=status.HTTP_201_CREATED, headers=headers)
        logger.info('Response create ERROR %s' %
                    (serializer.data['data_hash'] if 'data_hash' in
                     serializer.data else '',))
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
                    (serializer.data['data_hash'] if 'data_hash' in
                     serializer.data else '',))
        return self.get_error_response(serializer)

    def delete(self, request, *args, **kwargs):
        dev = False
        serializer = self.get_serializer(data=request.data)
        if serializer.check_code(kwargs['pk'], raise_exception=False):
            if hasattr(serializer.adr, "authenticaterequest"):
                serializer.adr.authenticaterequest.delete()
            if hasattr(serializer.adr, "signrequest"):
                serializer.adr.signrequest.delete()
            serializer.adr.delete()
            dev = True
        response = {'result': dev}
        headers = self.get_success_headers(response)
        return Response(self.get_encrypted_response(response, serializer),
                        status=status.HTTP_201_CREATED, headers=headers)

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
