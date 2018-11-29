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
@date: 13/9/2017
@author: Universidad de Costa Rica
@maintainer: Luis Zarate Montero
@contact: luis.zarate@solvosoft.com
@license: GPLv3
'''

from corebase.serializer import CheckBaseBaseSerializer, CoreBaseBaseSerializer
from institution.models import Institution, NotificationURL
from django.utils.translation import ugettext_lazy as _


import logging
from corebase.rsa import decrypt
from corebase.ca_management import check_certificate
from corebase.ciphers import Available_ciphers
from django.conf import settings

logger = logging.getLogger(settings.DEFAULT_LOGGER_NAME)


class InstitutionBaseSerializer(CoreBaseBaseSerializer):
    encrypt_method = None

    def check_subject(self):
        if self.institution is None:
            self._errors['data'] = [
                _('Institution not found, certificate does not match')]
            return False
        return True

    def get_institution(self):
        try:
            self.institution = Institution.objects.filter(
                code=self.data['institution']).first()
        except:
            logger.error("Get institution: Institution not found %r" %
                         (self.data['institution'] if 'institution' in
                          self.data else "No institution in data", ))
            self._errors['institution'] = [
                _('Institution not found, certificate does not match')]
            self.institution = None

    def _get_decrypt_key(self):
        return self.institution.server_sign_key

    def _check_internal_data(self, data, fields=[]):
        if data['institution'] != str(self.institution.code):
            self._errors['institution'] = [_('Institution does not match')]

        if data['notification_url'].upper() == 'N/D':
            if not NotificationURL.objects.filter(
                institution=self.institution,
                    not_webapp=True).exists():
                self._errors['notification_url'] = [
                    'notification_url not found']
        elif not NotificationURL.objects.filter(
                institution=self.institution,
                url=data['notification_url']).exists():
            self._errors['notification_url'] = [
                _('notification_url not found')]

    def get_encryption_cipher(self):
        available_ciphers = list(Available_ciphers.keys())
        self.encrypt_method = 'aes_eax'
        if 'encrypt_method' in self.data:
            if self.data['encrypt_method'] in available_ciphers:
                self.encrypt_method = self.data['encrypt_method']
            else:
                self._errors['encrypt_method'] = [
                    _('encrypt_method not found')]

    def validate_certificate(self):
        self.get_encryption_cipher()
        self.get_institution()
        if self.institution is None:
            self._errors['data'] = [
                _('Institution not found, certificate does not match')]
            return False
        if not check_certificate(self.data['public_certificate']):
            self._errors['public_certificate'] = [_('Invalid Certificate')]
        try:
            self.requestdata = decrypt(self.institution.server_sign_key,
                                       self.data['data'],
                                       method=self.encrypt_method)
            self.check_internal_data(
                self.requestdata, fields=self.check_internal_fields)
            self.check_received_extra_data(self.requestdata)
        except Exception as e:
            self._errors['data'] = [_('Data was not decrypted well')]
            logger.error('Data was not decrypted well %r' % (e,))
            return False


class InstitutionCheckBaseBaseSerializer(InstitutionBaseSerializer, CheckBaseBaseSerializer):
    pass
