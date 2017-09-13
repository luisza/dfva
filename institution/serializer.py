'''
Created on 13 sep. 2017

@author: luisza
'''
from corebase.serializer import CheckBaseBaseSerializer, CoreBaseBaseSerializer
from institution.models import Institution, NotificationURL
from django.utils.translation import ugettext_lazy as _
from corebase.ca_management.check_cert import check_certificate

import logging
from corebase.rsa import decrypt


logger = logging.getLogger('dfva')

class InstitutionBaseSerializer(CoreBaseBaseSerializer):

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
                         (self.data['institution'] if 'institution' in self.data else "No institution in data", ))
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

    def validate_certificate(self):
        self.get_institution()
        if self.institution is None:
            self._errors['data'] = [
                _('Institution not found, certificate does not match')]
            return False
        if not check_certificate(self.data['public_certificate']):
            self._errors['public_certificate'] = [_('Invalid Certificate')]
        try:
            self.requestdata = decrypt(self.institution.server_sign_key,
                                       self.data['data'])
            self.check_internal_data(
                self.requestdata, fields=self.check_internal_fields)
        except Exception as e:
            self._errors['data'] = [_('Data was not decrypted well')]
            logger.error('Data was not decrypted well %r' % (e,))
            return False


class InstitutionCheckBaseBaseSerializer(InstitutionBaseSerializer, CheckBaseBaseSerializer):
    pass
