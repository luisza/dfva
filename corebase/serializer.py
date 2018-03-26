'''
Created on 18 jul. 2017

@author: luis
'''
from corebase.rsa import get_hash_sum,  decrypt
from corebase.models import ALGORITHM
from rest_framework import serializers
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
import logging
from corebase.ca_management import check_certificate

logger = logging.getLogger('dfva')


class CoreBaseBaseSerializer(object):

    def validate_digest(self):
        hashsum = get_hash_sum(self.data['data'], self.data['algorithm'])
        if hashsum != self.data['data_hash']:
            self._errors['data_hash'] = [
                _('Hash sums are not equal %s != %s') % (hashsum, self.data['data_hash'])]
            # FIXME:  Hay que hacer algo con los errores de status

    def _get_decrypt_key(self):
        return

    def get_institution(self):
        pass

    def check_subject(self):
        return True

    def check_internal_data(self, data, fields=[]):
        for field in fields:
            if field not in data:
                self._errors[field] = ['%s not found' % (field)]
        self._check_internal_data(data, fields=self.check_internal_fields)
        self.check_hash_algorithm(data)

    def check_hash_algorithm(self, data):
        if 'algorithm_hash' in data:
            supported_algorithm = [x for x, y in ALGORITHM]
            if data['algorithm_hash'] not in supported_algorithm:
                self._errors['data'] = [
                    _('%s is not valid algorithm. supported are %s ') % (
                        data['algorithm_hash'],
                        ",".join(
                            supported_algorithm)
                    )]

    def validate_certificate(self):
        self.get_institution()
        if self.check_subject():
            if not check_certificate(self.data['public_certificate']):
                self._errors['public_certificate'] = [
                    _('Invalid certificate')]
            try:
                
                self.requestdata = decrypt(self._get_decrypt_key(),
                                           self.data['data'])
                logger.debug("Data: %r" % (self.requestdata,))
                self.check_internal_data(self.requestdata)
            except Exception as e:
                self._errors['data'] = [
                    _('Data was not decrypted well %r') % (e,)]
                logger.error('Data was not decrypted well %r' % (e,))
                return False

    def is_valid(self, raise_exception=False):
        serializers.HyperlinkedModelSerializer.is_valid(
            self, raise_exception=raise_exception)
        self.validate_digest()
        self.validate_certificate()

        if self._errors and raise_exception:
            raise ValidationError(self.errors)
        return not bool(self._errors)


class CheckBaseBaseSerializer():

    def check_code(self, code, raise_exception=False):
        dev = False
        self.check_internal_fields = self.check_show_fields

        if self.is_valid(raise_exception=raise_exception):
            fields = {
               
                'id_transaction': code,
                #'identification': self.requestdata['identification'],
                'expiration_datetime__gte': timezone.now()
            }
           
            # fixme: Revisar si se debe hacer esta comprobacion
            # cuando se trata de una persona firmante
            #if 'identification' in self.requestdata:
            #    fields['identification'] = self.requestdata['identification']

            if hasattr(self.validate_data_class, 'institution'):
                fields['institution']= self.institution
            
            if 'notification_url' in self.check_internal_fields:
                fields['notification_url'] = self.requestdata['notification_url']
            data = self.validate_data_class.objects.filter(
                **fields).first()
            if data:
                self.adr = data
                dev = True
                
        return dev
