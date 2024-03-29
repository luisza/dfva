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

import logging

from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from pyfva.clientes.validadorv2 import ClienteValidador
from rest_framework import serializers
from rest_framework.authtoken.models import Token

from corebase.rsa import pem_to_base64, validate_sign
from corebase.serializer import CoreBaseBaseSerializer, CheckBaseBaseSerializer
from institution.models import Institution
from person.models import Person, PersonLogin
import random

logger = logging.getLogger(settings.DEFAULT_LOGGER_NAME)


class OperandLogin:
    operands = ['+', '-', '*', '/', '%', '//']

    @classmethod
    def operate(cls, oper1, oper2, oper):
        dev = 0
        if oper not in cls.operands:
            return

        if oper == '+':
            dev = oper1+oper2
        elif oper == '-':
            dev = oper1-oper2
        elif oper == '*':
            dev = oper1*oper2
        elif oper == '/':
            dev = oper1/oper2
        elif oper == '%':
            dev = oper1%oper2
        elif oper == '//':
            dev = oper1//oper2
        return dev
    @classmethod
    def get_operand(cls):
        num = random.randint(0, len(cls.operands)-1)
        return cls.operands[num]


class PersonBaseSerializer(CoreBaseBaseSerializer):

    def validate_digest(self):
        self.requestdata = self.data['data']

    def validate_certificate(self):
        client = ClienteValidador(
            negocio=settings.DEFAULT_BUSSINESS,
            entidad=settings.DEFAULT_ENTITY,
        )
        if client.validar_servicio('certificado'):
            data = client.validar_certificado_autenticacion(pem_to_base64(self.data['public_certificate']))
        else:
            logger.warning("Certificate BCCR not available")
            data = client.DEFAULT_CERTIFICATE_ERROR
            self._errors['public_certificate'] = [_("Wrong certificate or communication error")]

        if data['codigo_error'] != 0 or not data['exitosa']:
            self._errors['public_certificate'] = [_('Invalid certificate')]

        if self.check_subject():
            self.check_internal_data(self.requestdata)

    def get_person(self):
        self.person = Person.objects.filter(identification=self.data['person']).first()
        if self.person is None:
            self._errors['data'] = [
                _('User not registered in the system')]

    def check_subject(self):
        return True
    # Fixme: Revisar que persona exista

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
    transaction_id = serializers.IntegerField(required=True)

    def get_transaction(self):
        self.transaction = PersonLogin.objects.filter(pk=self.data['transaction_id'], person=self.data['person']).first()
        if self.transaction is None:
            self._errors['transaction_id'] = 'Transaction ID not found'

    def get_person(self, cert_data):
        if self.person is not None:
            return self.person

        if 'person' in self.data:
            self.person = Person.objects.filter(identification=self.data['person']).first()
            if self.person is None:
                user = User.objects.filter(username=self.data['person']).first()
                if user is None:
                    user = User.objects.create_user(self.data['person'])
                user.first_name = cert_data['certificado']['nombre']
                user.save()
                # Fixme: mejor forma de captar el nombre
                self.person = Person.objects.create(user=user, identification=self.data['person'])
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

        plain_text = str(OperandLogin.operate(
            self.transaction.operatorA, self.transaction.operatorB, self.transaction.operand ))
        if not validate_sign(self.data['public_certificate'],
                             plain_text, self.data['code']):
            self._errors['data_hash'] = [
                _('Data hash invalid, are you signing with your private key \
                pair?')]
            return False
        return True

    def is_valid(self, raise_exception=False):
        serializers.HyperlinkedModelSerializer.is_valid(
            self, raise_exception=raise_exception)

        self.get_transaction()
        if self.transaction:
            if self.validate_digest():
                ok, data = self.validate_certificate()
                if ok:
                    self.get_person(data)
        if self._errors and raise_exception:
            raise ValidationError(self.errors)
        return not bool(self._errors)



    def save(self):
        person = self.person

        token, created = Token.objects.get_or_create(user=self.person.user)
        logger.debug("Token: "+token.key)
        person.token = token.key
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
            'public_certificate', 'code', 'person', 'data_hash', 'algorithm', 'transaction_id'
        )


class PersonLoginResponseSerializer(serializers.HyperlinkedModelSerializer):
    token = serializers.CharField()

    class Meta:
        model = Person
        fields = (
            'identification',
            'token',
            'expiration_datetime_token',
            'last_error_code'
        )
