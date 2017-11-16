'''
Created on 13 sep. 2017

@author: luisza
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
import logging
# FIXME: Quitar de aquí institution
from institution.models import Institution
from django.contrib.auth.models import User

logger = logging.getLogger('dfva')


class PersonBaseSerializer(CoreBaseBaseSerializer):

    def validate_digest(self):
        super(PersonBaseSerializer, self).validate_digest()
        try:
            plain_text = self._get_decrypt_key()
        except:
            self._errors['data'] = [_('Sign, wrong encryption')]
            return
        if not validate_sign_data(self.data['public_certificate'], plain_text, self.data['data']):
            self._errors['data_hash'] = [
                _('Sign key check fail,  are you signing with your private key pair?')]

    def validate_certificate(self):
        self.get_institution()
        client = ClienteValidador(
            negocio=self.institution.bccr_bussiness,
            entidad=self.institution.bccr_entity,
        )
        if client.validar_servicio('certificado'):

            data = client.validar_certificado_autenticacion(
                pem_to_base64(self.data['public_certificate']))

        else:
            logger.warning("Certificate BCCR not available")
            data = client.DEFAULT_CERTIFICATE_ERROR
            self._errors['public_certificate'] = [
                _("Wrong certificate or communication error")]

        if data['codigo_error'] != 1 or not data['exitosa']:
            self._errors['public_certificate'] = [_('Invalid certificate')]

        if self.check_subject():

            try:
                key = self._get_decrypt_key()
                self.requestdata = decrypt_person(self.data['public_certificate'], key,
                                                  self.data['data'])
                self.check_internal_data(self.requestdata)
            except Exception as e:
                self._errors['data'] = [
                    _('Data was not decrypted well %r') % (e,)]
                return False

    def get_institution(self):
        self.institution = Institution.objects.first()
        self.person = Person.objects.filter(
            identification=self.data['person']).first()

    def check_subject(self):
        return True
    # Fixme: Revisar que pesona exista

    def _get_decrypt_key(self):
        self.get_institution()
        key = decrypt(self.institution.private_key,
                      self.person.cipher_token, as_str=False)
        return key

    def _check_internal_data(self, data, fields=[]):
        self.person = Person.objects.filter(
            identification=data['person']).first()
        if self.person is None:
            self._errors['person'] = [_('Person not found')]


class PersonCheckBaseBaseSerializer(PersonBaseSerializer,  CheckBaseBaseSerializer):
    pass


class PersonLoginSerializer(serializers.HyperlinkedModelSerializer):

    def get_institution(self):
        self.institution = Institution.objects.first()
        
        if 'person' in self.data:
            self.person = Person.objects.filter(
            identification=self.data['person']).first()
            if self.person is None:
                ok, data=self.validate_certificate()
                if ok:
                    user=User.objects.create_user(self.data['person'])
                    user.first_name=data['nombre']
                    user.save()
                    #Fixme: mejor forma de captar el nombre
                    self.person = Person.objects.create(
                        user=user,
                        identification=self.data['person'])
    
    def validate_certificate(self):
        client = ClienteValidador(
            negocio=self.institution.bccr_bussiness,
            entidad=self.institution.bccr_entity,
        )
        if client.validar_servicio('certificado'):

            data = client.validar_certificado_autenticacion(
                pem_to_base64(self.data['public_certificate']))

        else:
            logger.warning("Login certificate BCCR not available")
            data = client.DEFAULT_CERTIFICATE_ERROR
        dev=True
        if data['codigo_error'] != 1 or not data['exitosa']:
            self._errors['public_certificate'] = [_('Invalid certificate')]
            dev=False

        elif data['certificado']['identificacion'] != self.data['person']:
            self._errors['public_certificate'] = [
                _('Signer certificate is not owned by person who request')]
            dev=False
        return dev, data

    def validate_digest(self):
        # Fixme: Solo funciona para register
        plain_text = self.data['person']
        if not validate_sign(self.data['public_certificate'], plain_text, self.data['code']):
            self._errors['data_hash'] = [
                _('Data hash invalid, are you signing with your private key pair?')]

    def is_valid(self, raise_exception=False):
        serializers.HyperlinkedModelSerializer.is_valid(
            self, raise_exception=raise_exception)

        self.get_institution()
        self.validate_certificate()
        self.validate_digest()
        if self._errors and raise_exception:
            raise ValidationError(self.errors)
        return not bool(self._errors)

    def save(self):
        person = Person.objects.get(identification=self.data['person'])
        random_token = get_random_token()
        person.cipher_token = encrypt(self.institution.public_key,
                                      random_token
                                      )
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
