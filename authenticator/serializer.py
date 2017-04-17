# encoding: utf-8


'''
Created on 14/4/2017

@author: luisza
'''
from __future__ import unicode_literals

import datetime

from django.conf import settings
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from authenticator.models import AuthenticateDataRequest, AuthenticateRequest,\
    Institution, NotificationURL
from ca.ca_management.check_cert import check_certificate
from ca.rsa import decrypt, get_hash_sum


class Authenticate_Request_Serializer(serializers.HyperlinkedModelSerializer):
    data = serializers.CharField(
        help_text="""Datos de solicitud de autenticación encriptados: los datos son
        {institution: uid de la institucion ver code en detalles de institución,
        notification_url: URL para la notificación Nota debe estar inscrita,
        identification: Identificación de la persona a autenticar,
        request_datetime: Hora de petición en formato '%Y-%m-%d %H:%M:%S', osea  '2006-10-25 14:30:59'
         }
        
         """)
    readonly_fields = ['data']

    def validate_digest(self):
        hashsum = get_hash_sum(self.data['data'], self.data['algorithm'])
        if hashsum != self.data['data_hash']:
            self._errors['data_hash'] = [
                'Hash sum are not equals %s != %s' % (hashsum, self.data['data_hash'])]
            # HAy que hacer algo con los errores de status

    def check_internal_data(self, data):
        fields = ['notification_url', 'identification',
                  'request_datetime', 'institution']
        for field in fields:
            if field not in data:
                self._errors[field] = ['%s not found' % (field)]

        if data['institution'] != str(self.institution.code):
            self._errors['institution'] = ['Institution not match']

        if not NotificationURL.objects.filter(
                institution=self.institution,
                url=data['notification_url']).exists():
            self._errors['notification_url'] = ['notification_url not found']

    def validate_certificate(self):
        self.institution = Institution.objects.filter(
            code=self.data['institution']).first()
        if self.institution is None:
            self._errors['data'] = [
                'Institution not found, certificate not match']
            return False

        if not check_certificate(self.data['public_certificate']):
            self._errors['public_certificate'] = ['Certificate not valid']
        try:
            self.requestdata = decrypt(self.institution.server_sign_key,
                                       self.data['data'])
            self.check_internal_data(self.requestdata)
        except:
            self._errors['data'] = ['Data not decripted well']
            return False

    def is_valid(self, raise_exception=False):
        serializers.HyperlinkedModelSerializer.is_valid(
            self, raise_exception=raise_exception)
        self.validate_digest()
        self.validate_certificate()
        if self._errors and raise_exception:
            raise ValidationError(self.errors)
        return not bool(self._errors)

    def save(self, **kwargs):
        odata = {}
        for field in self.Meta.fields:
            if field == 'data':
                continue
            odata[field] = self.data[field]

        auth_request = AuthenticateRequest(**odata)

        adr = AuthenticateDataRequest()
        adr.notification_url = self.requestdata['notification_url']
        adr.identification = self.requestdata['identification']
        adr.institution = self.institution
        adr.request_datetime = parse_datetime(
            self.requestdata['request_datetime'])

        adr.expiration_datetime = timezone.now(
        ) + datetime.timedelta(minutes=settings.EXPIRED_DELTA)

        adr.save()
        self.adr = adr
        auth_request.data_request = adr
        auth_request.save()
        return auth_request

    class Meta:
        model = AuthenticateRequest
        fields = ('institution', 'data_hash', 'algorithm',
                  'public_certificate', 'data')


class Authenticate_Response_Serializer(serializers.ModelSerializer):

    class Meta:
        model = AuthenticateDataRequest
        fields = (
            'code', 'status', 'identification', 'name', 'request_datetime', 'expiration_datetime')
