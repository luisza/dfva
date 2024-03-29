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
from django.forms import modelform_factory

from corebase.rsa import get_hash_sum,  decrypt
from corebase.models import ALGORITHM
from rest_framework import serializers
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
import logging
from corebase.ca_management import check_certificate
from django.conf import settings
from corebase.time import parse_datetime

from corebase import  logger


class CoreBaseBaseSerializer(object):
    status_code = -1
    time_messages = {}

    def validate_digest(self):
        self.time_messages['start_hashsum'] = timezone.now()
        hashsum = get_hash_sum(self.data['data'], self.data['algorithm'])
        self.time_messages['end_hashsum'] = timezone.now()
        if hashsum != self.data['data_hash']:
            self._errors['data_hash'] = [
                _('Hash sums are not equal %(hashsum)s != %(datahash)s') % {'hashsum':hashsum,
                                                         'datahash':self.data['data_hash']}]
            # FIXME:  Hay que hacer algo con los errores de status

    def _get_decrypt_key(self):
        return

    def get_institution(self):
        pass

    def check_subject(self):
        return True

    def check_received_extra_data(self, data):
        pass

    def get_form(self):
        return self.form

    def check_form_data(self):
          if hasattr(self, 'requestdata') and self.requestdata:
            data = {}
            data.update(self.requestdata)
            if 'request_datetime' in data:
                data['request_datetime'] = parse_datetime(
                self.requestdata['request_datetime'])

            form = self.get_form()
            form = form(data)
            if not form.is_valid():
                if 'identification' in form.errors:
                    self.status_code = 10

                self._errors['data_internal'] = [form.errors.as_json()]

    def check_internal_data(self, data, fields=[]):
        for field in fields:
            if field not in data:
                self._errors[field] = ['%s not found' % (field)]
        self._check_internal_data(data, fields=self.check_internal_fields)
        self.check_hash_algorithm(data)
        self.check_received_extra_data(data)


    def check_hash_algorithm(self, data):
        if 'algorithm_hash' in data:
            supported_algorithm = [x for x, y in ALGORITHM]
            if data['algorithm_hash'] not in supported_algorithm:
                self._errors['data'] = [
                    _('%(algorithm_hash)s is not valid algorithm. supported are %(supported_algo)s ') %
                    {
                      'algorithm_hash':  data['algorithm_hash'],
                       'supported_algo': ",".join( supported_algorithm)
                    }]

    def validate_certificate(self):
        self.get_institution()
        if self.check_subject():
            self.time_messages['start_check_institution_certificate'] = timezone.now()
            if not check_certificate(self.data['public_certificate']):
                self._errors['public_certificate'] = [
                    _('Invalid certificate')]
                logger.info({"message": "Validate certificate invalid certificate",
                              'data': repr(self.data['public_certificate']), 'location': __file__})
            self.time_messages['end_check_institution_certificate'] = timezone.now()
            try:
                self.time_messages['start_decrypt'] = timezone.now()
                self.requestdata = decrypt(self._get_decrypt_key(),
                                           self.data['data'],
                                           method=self.encrypt_method)
                self.time_messages['end_decrypt'] = timezone.now()
                logger.debug({"message": "Validate certificate data",
                              'data': self.requestdata, 'location': __file__})
                self.check_internal_data(self.requestdata)
            except Exception as e:
                self.requestdata = None
                self._errors['data'] = [
                    _('Data was not decrypted well %r') % (e,)]
                logger.error({'message':'Validate certificate data was not decrypted well',
                              'data': repr(e), 'location': __file__})
                return False

    def is_valid(self, raise_exception=False):
        serializers.HyperlinkedModelSerializer.is_valid(
            self, raise_exception=raise_exception)
        self.validate_digest()
        self.validate_certificate()
        self.check_form_data()
        if self._errors and raise_exception:
            raise ValidationError(self.errors)
        return not bool(self._errors)


class CheckBaseBaseSerializer:
    code_id_name = 'id_transaction'

    def check_code(self, code, raise_exception=False):
        dev = False
        self.check_internal_fields = self.check_show_fields
        self.form = self.form_check

        if self.is_valid(raise_exception=raise_exception):
            fields = {
                self.code_id_name: code,
                'expiration_datetime__gte': timezone.now()
            }

            # fixme: Revisar si se debe hacer esta comprobacion
            # cuando se trata de una persona firmante
            # if 'identification' in self.requestdata:
            #    fields['identification'] = self.requestdata['identification']

            if hasattr(self.validate_data_class, 'institution'):
                fields['institution'] = self.institution

            if 'notification_url' in self.check_internal_fields:
                fields['notification_url'] = self.requestdata['notification_url']
            data = self.validate_data_class.objects.filter(
                **fields).first()
            if data:
                self.adr = data
                dev = True

        return dev
