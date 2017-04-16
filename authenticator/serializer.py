# encoding: utf-8


'''
Created on 14/4/2017

@author: luisza
'''
from __future__ import unicode_literals

import hashlib

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from authenticator.models import Institution
from ca.rsa import decrypt, get_hash_sum

from .models import Authenticate_Request


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

    def validate_certificate(self):
        institution = Institution.objects.filter(
            code=self.data['institution']).first()
        if institution is None:
            self._errors['data'] = [
                'Institution not found, certificate not match']
            return False

        try:
            data = decrypt(institution.server_sign_key,
                           self.data['data'])

        except Exception as e:
            print (e)
            self._errors['data'] = ['Data not decripted well']

    def is_valid(self, raise_exception=False):
        valid = serializers.HyperlinkedModelSerializer.is_valid(
            self, raise_exception=raise_exception)
        self.validate_digest()
        self.validate_certificate()
        if self._errors and raise_exception:
            raise ValidationError(self.errors)
        return not bool(self._errors)

    class Meta:
        model = Authenticate_Request
        fields = ('institution', 'data_hash', 'algorithm',
                  'public_certificate', 'data')


class Authenticate_Response_Serializer(serializers.ModelSerializer):

    class Meta:
        model = Authenticate_Request
        fields = ('code', 'status', 'arrived_time', 'expirate_datetime')
