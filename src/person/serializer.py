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
@author: Luis Zarate Montero
@contact: luis.zarate@solvosoft.com
@license: GPLv3
'''

from corebase.serializer import CoreBaseBaseSerializer, CheckBaseBaseSerializer
from corebase.rsa import validate_sign_data, pem_to_base64, decrypt_person,\
    rsa_encrypt, get_random_token, validate_sign, decrypt, encrypt
from pyfva.clientes.validador import ClienteValidador
from rest_framework import serializers
from django.utils.translation import ugettext_lazy as _
from person.models import Person, PersonLogin
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.conf import settings
from django.contrib.auth.models import User
from base64 import b64encode

import logging
from institution.models import Institution
logger = logging.getLogger(settings.DEFAULT_LOGGER_NAME)


class PersonBaseSerializer(CoreBaseBaseSerializer):

    def validate_digest(self):
        super(PersonBaseSerializer, self).validate_digest()
        try:
            plain_text = self._get_decrypt_key()
        except Exception as enc:
            self._errors['data'] = [_('Sign, wrong encryption')]
            logger.debug("Sign, wrong encryption %r " % (enc,))
            return
        if not validate_sign_data(self.data['public_certificate'],
                                  plain_text, self.data['data']):
            self._errors['data_hash'] = [
                _('Sign key check fail,  are you signing with your \
                private key pair?')]

    def validate_certificate(self):
        self.get_institution()
        client = ClienteValidador(
            negocio=settings.DEFAULT_BUSSINESS,
            entidad=settings.DEFAULT_ENTITY,
        )
        if client.validar_servicio('certificado'):

            data = client.validar_certificado_autenticacion(
                pem_to_base64(self.data['public_certificate']))

        else:
            logger.warning("Certificate BCCR not available")
            data = client.DEFAULT_CERTIFICATE_ERROR
            self._errors['public_certificate'] = [
                _("Wrong certificate or communication error")]

        if data['codigo_error'] != 0 or not data['exitosa']:
            self._errors['public_certificate'] = [_('Invalid certificate')]

        if self.check_subject():

            try:
                key = self._get_decrypt_key()
                self.requestdata = decrypt_person(
                    self.data['public_certificate'], key,
                    self.data['data'])
                self.check_internal_data(self.requestdata)
            except Exception as e:
                self._errors['data'] = [
                    _('Data was not decrypted well %r') % (e,)]
                return False

    def get_person(self):
        self.person = Person.objects.filter(
            identification=self.data['person']).first()
        if self.person is None:
            self._errors['data'] = [
                _('User not registered in the system')]

    def check_subject(self):
        return True
    # Fixme: Revisar que pesona exista

    def get_private_key(self):
        keyenc = None
        with open(settings.DFVA_KEY_PATH, 'rb') as arch:
            keyenc = arch.read()
        return keyenc

    def _get_decrypt_key(self):

        self.get_person()
        key = decrypt(self.get_private_key(),
                      self.person.cipher_token, as_str=False)
        return key

    def _check_internal_data(self, data, fields=[]):
        self.get_person()
        if self.person is None:
            self._errors['person'] = [_('Person not found')]

    def get_institution(self):
        self.institution = Institution.objects.first()
        return self.institution


class PersonCheckBaseBaseSerializer(PersonBaseSerializer,
                                    CheckBaseBaseSerializer):
    pass


class PersonLoginSerializer(serializers.HyperlinkedModelSerializer):
    person = None

    def get_person(self):
        if self.person is not None:
            return self.person

        if 'person' in self.data:
            self.person = Person.objects.filter(
                identification=self.data['person']).first()
            if self.person is None:
                ok, data = self.validate_certificate()
                if ok:
                    user = User.objects.filter(
                        username=self.data['person']).first()
                    if user is None:
                        user = User.objects.create_user(self.data['person'])
                    user.first_name = data['certificado']['nombre']
                    user.save()
                    # Fixme: mejor forma de captar el nombre
                    self.person = Person.objects.create(
                        user=user,
                        identification=self.data['person'])
        return self.person

    def validate_certificate(self):
        client = ClienteValidador(
            negocio=settings.DEFAULT_BUSSINESS,
            entidad=settings.DEFAULT_ENTITY,
        )
        if client.validar_servicio('certificado'):

            data = client.validar_certificado_autenticacion(
                pem_to_base64(self.data['public_certificate']))

        else:
            logger.warning("Login certificate BCCR not available")
            data = client.DEFAULT_CERTIFICATE_ERROR
        dev = True

        if data['codigo_error'] != 0 or not data['exitosa']:
            self._errors['public_certificate'] = [_('Invalid certificate')]
            dev = False

        elif data['certificado']['identificacion'] != self.data['person']:
            self._errors['public_certificate'] = [
                _('Signer certificate is not owned by person who request')]
            dev = False
        return dev, data

    def validate_digest(self):
        # Fixme: Solo funciona para register
        plain_text = self.data['person']
        if not validate_sign(self.data['public_certificate'],
                             plain_text, self.data['code']):
            self._errors['data_hash'] = [
                _('Data hash invalid, are you signing with your private key \
                pair?')]

    def is_valid(self, raise_exception=False):
        serializers.HyperlinkedModelSerializer.is_valid(
            self, raise_exception=raise_exception)

        self.get_person()
        self.validate_certificate()
        self.validate_digest()
        if self._errors and raise_exception:
            raise ValidationError(self.errors)
        return not bool(self._errors)

    def get_public_key(self):
        public_key = None
        with open(settings.DFVA_CERT_PATH, 'r') as arch:
            public_key = arch.read()

        return public_key

    def save(self):
        person = self.get_person()
        random_token = get_random_token()
        person.cipher_token = encrypt(self.get_public_key(),
                                      random_token
                                      )
        logger.debug("Token: "+person.identification+" => " +
                     b64encode(random_token).decode('utf-8'))
        person.token = rsa_encrypt(
            self.data['public_certificate'], message=random_token).decode()
        person.authenticate_certificate = self.data['public_certificate']
        person.expiration_datetime_token = timezone.now(
        ) + timezone.timedelta(minutes=settings.DFVA_PERSON_SESSION)
        person.last_error_code = 1
        person.save()
        response = PersonLoginResponseSerializer(person)

        return response

    class Meta:
        model = PersonLogin
        fields = (
            'public_certificate', 'code', 'person', 'data_hash', 'algorithm'
        )


class PersonLoginResponseSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Person
        fields = (
            'identification',
            'token',
            'expiration_datetime_token',
            'last_error_code'
        )
