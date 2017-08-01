'''
Created on 18 jul. 2017

@author: luis
'''
from corebase.rsa import get_hash_sum, decrypt
from corebase.models import NotificationURL, Institution, ALGORITHM
from corebase.ca_management.check_cert import check_certificate
from rest_framework import serializers
from django.core.exceptions import ValidationError


class CoreBaseBaseSerializer(object):

    def validate_digest(self):
        hashsum = get_hash_sum(self.data['data'], self.data['algorithm'])
        if hashsum != self.data['data_hash']:
            self._errors['data_hash'] = [
                'Hash sum are not equals %s != %s' % (hashsum, self.data['data_hash'])]
            # FIXME:  Hay que hacer algo con los errores de status

    def _check_internal_data(self, data, fields=[]):

        for field in fields:
            if field not in data:
                self._errors[field] = ['%s not found' % (field)]

        if data['institution'] != str(self.institution.code):
            self._errors['institution'] = ['Institution not match']

        if data['notification_url'].upper() == 'N/D':
            if not NotificationURL.objects.filter(
                institution=self.institution,
                    not_webapp=True).exists():
                self._errors['notification_url'] = [
                    'notification_url not found']
        elif not NotificationURL.objects.filter(
                institution=self.institution,
                url=data['notification_url']).exists():
            self._errors['notification_url'] = ['notification_url not found']

    def check_internal_data(self, data, fields=[]):
        self._check_internal_data(data, fields=self.check_internal_fields)
        self.check_hash_algorithm(data)

    def check_hash_algorithm(self, data):
        if 'algorithm_hash' in data:
            supported_algorithm = [x for x, y in ALGORITHM]
            if data['algorithm_hash'] not in supported_algorithm:
                self._errors['data'] = [
                    '%s is not valid algorithm. supported are %s ' % (
                        data['algorithm_hash'],
                        ",".join(
                            supported_algorithm)
                    )]

    def get_institution(self):
        self.institution = Institution.objects.filter(
            code=self.data['institution']).first()

    def validate_certificate(self):
        self.get_institution()
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
        except Exception as e:
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


class CoreCheckBaseBaseSerializer(CoreBaseBaseSerializer):

    def check_code(self, code, raise_exception=False):
        dev = False
        self.check_internal_fields = self.check_show_fields
        if self.is_valid(raise_exception=raise_exception):
            fields = {
                'code': code,
                'identification': self.requestdata['identification']
            }
            if 'notification_url' in self.check_internal_fields:
                fields['notification_url'] = self.requestdata['notification_url']
            data = self.validate_data_class.objects.filter(
                **fields).first()
            if data:
                self.adr = data
                dev = True
        return dev
