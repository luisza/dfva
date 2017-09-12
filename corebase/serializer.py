'''
Created on 18 jul. 2017

@author: luis
'''
from corebase.rsa import get_hash_sum, decrypt, rsa_encrypt, get_random_token,\
    encrypt, validate_sign, pem_to_base64, decrypt_person, validate_sign_data
from corebase.models import NotificationURL, Institution, ALGORITHM, Person,\
    PersonLogin
from corebase.ca_management.check_cert import check_certificate
from rest_framework import serializers
from django.core.exceptions import ValidationError
from django.utils import timezone
from pyfva.clientes.validador import ClienteValidador
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
import logging

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
                self.requestdata = decrypt_person(key,
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
        # Fixme: check person in self.data first
        self.person = Person.objects.get(
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

        if data['codigo_error'] != 1 or not data['exitosa']:
            self._errors['public_certificate'] = [_('Invalid certificate')]

        elif data['certificado']['identificacion'] != self.data['person']:
            self._errors['public_certificate'] = [
                _('Signer certificate is not owned by person who request')]

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
