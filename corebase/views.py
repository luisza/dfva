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
from corebase.models import PersonLogin
from corebase.serializer import PersonLoginSerializer,\
    PersonLoginResponseSerializer


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
    def get_success_headers(self, data):
        try:
            return {'Location': data[api_settings.URL_FIELD_NAME]}
        except (TypeError, KeyError):
            return {}

    def _create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        headers = self.get_success_headers(serializer.data)
        adr = self.response_class(serializer.adr)
        # adr.is_valid(raise_exception=False)
        return Response(adr.data, status=status.HTTP_201_CREATED, headers=headers)

    def show(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.check_code(kwargs['pk'], raise_exception=True):
            headers = self.get_success_headers(serializer.data)
            adr = self.response_class(serializer.adr)
            # adr.is_valid(raise_exception=False)
            return Response(adr.data, status=status.HTTP_201_CREATED, headers=headers)

        return self.get_error_response()

    def get_error_response(self):
        return Response({"error": "Error inexperado"})


class PersonLoginView(mixins.CreateModelMixin,
                      viewsets.GenericViewSet):

    queryset = PersonLogin.objects.all()
    serializer_class = PersonLoginSerializer
    response_class = PersonLoginResponseSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            data = serializer.save()
            headers = self.get_success_headers(data.data)
            return Response(data.data, status=status.HTTP_201_CREATED, headers=headers)

        return Response({
            'identification': 'N/D',
            'token': None,
            'expiration_datetime_token': None,
            'last_error_code': 3
        }, status=status.HTTP_201_CREATED, headers=headers)
