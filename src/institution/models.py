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
@date: 14/4/2017
@author: Universidad de Costa Rica
@maintainer: Luis Zarate Montero
@contact: luis.zarate@solvosoft.com
@license: GPLv3
'''

from dateutil.relativedelta import relativedelta
from django.db import models
from django.utils import timezone
from corebase.models import identification_validator, BaseDocument, \
    BaseRequestModel, BaseAuthenticate, BaseSign, BaseValidateCertificate, BaseStamp
from institution.presentation import PEMpresentation
from django.contrib.auth.models import User
import uuid
from django.conf import settings
from corebase.rsa import salt_decrypt, salt_encrypt
from asn1crypto import pem,  x509
from dateutil.parser import parse
from pyfva import constants


class EncrytedText(models.TextField):

    def from_db_value(self, value, expression, connection):
        if isinstance(value, str):
            value = value.encode()
        return salt_decrypt(value)

    def pre_save(self, model_instance, add):
        field = getattr(model_instance, self.attname)
        dev = salt_encrypt(field)
        if type(dev) == bytes:
            dev = dev.decode()
        return dev

    def value_from_object(self, obj):
        dev = super(EncrytedText, self).value_from_object(obj)
        return dev.decode()



class Institution(models.Model, PEMpresentation):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=250, verbose_name="Nombre de la aplicación")
    code = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, verbose_name="Código")
    active = models.BooleanField(default=True, verbose_name="Está activo")
    bccr_bussiness = models.IntegerField(default=settings.DEFAULT_BUSSINESS, verbose_name="Negocio para BCCR")
    bccr_entity = models.IntegerField(default=settings.DEFAULT_ENTITY, verbose_name="Entidad para BCCR")

    domain = models.CharField(max_length=250, verbose_name="Dominio para el certificado ej. servicio.ucr.ac.cr")  # Certificate domain
    institution_unit = models.CharField(
        max_length=250, default="ND", verbose_name="Unidad en el certificado")  # UO in cert
    private_key = models.TextField()
    public_key = EncrytedText()
    public_certificate = EncrytedText()
    server_sign_key = EncrytedText()
    server_public_key = EncrytedText()

    email = models.EmailField(verbose_name="Correo electrónico")
    phone = models.CharField(max_length=25, null=True, blank=False, verbose_name="Teléfono de contacto")
    administrative_institution = models.BooleanField(default=False)
    can_stamp = models.BooleanField(default=False, verbose_name="Puede sellar electrónicamente")

    def __str__(self):
        return self.name

    def get_expiration_date(self):
        if not self.administrative_institution:
            _, _, certificate_bytes = pem.unarmor(
                self.public_certificate, multiple=False)
            cert = x509.Certificate.load(certificate_bytes)
            certdate = cert.native['tbs_certificate']['validity']['not_after']
        else:
            certdate = timezone.now() + relativedelta(years=1)
        return certdate

    class Meta:
        ordering = ('pk',)


class NotificationURL(models.Model):
    description = models.CharField(max_length=250, verbose_name="Descripción")
    url = models.URLField(null=True, blank=True)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    not_webapp = models.BooleanField(default=False, verbose_name="Sin URL de notificiación")
    is_demo = models.BooleanField(default=False, verbose_name="Es demo")

    def __str__(self):
        return "%s %s" % (
            self.institution.name,
            self.url or 'N/D'
        )

    class Meta:
        ordering = ('institution',)


class InstitutionStats(models.Model):
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    datetime = models.DateTimeField(auto_now_add=True)
    status = models.SmallIntegerField(default=1, verbose_name="Estado")
    notified = models.BooleanField(default=False, verbose_name="Notificado")
    transaction_id = models.IntegerField()
    data_type = models.SmallIntegerField(choices=(
        (0, 'Autenticación'),
        (1, 'Firma'),
        (2, 'Validación de certificado'),
        (3, 'Validación de documento')
    ))
    document_type = models.CharField(
        max_length=15, default="n/d"
    )

    was_successfully = models.BooleanField(default=False)


class BaseInstitutionRequestModel(BaseRequestModel):
    CIPHERS = (
        ("aes_eax", "aes_eax (recomendado)"),
        ("aes-256-cfb", "aes-256-cfb")
    )
    public_certificate = models.TextField(
        help_text="""Certificado público de la institución (ver Institución) """)
    institution = models.CharField(
        max_length=50, help_text="UUID de la institución")
    encrypt_method = models.CharField(max_length=25,
                                      choices=CIPHERS,
                                      default='aes_eax',
                                      blank=True)

    class Meta:
        abstract = True


class AuthenticateDataRequest(BaseAuthenticate):
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    notification_url = models.URLField()

    def __str__(self):
        return repr(self)

    def __repr__(self):
        return "AuthenticateDataRequest(%d)  %s %r %d" % (
            self.id_transaction,
            self.identification,
            self.code,
            self.status
        )

    @property
    def left_time(self):
        now = timezone.now()
        ttime = relativedelta(self.expiration_datetime, now)
        return "%d:%d:%d" % (ttime.hours, ttime.minutes, ttime.seconds)

    class Meta:
        ordering = ('request_datetime',)


class AuthenticateRequest(BaseInstitutionRequestModel):
    data_request = models.OneToOneField(
        AuthenticateDataRequest,
        on_delete=models.CASCADE,
        null=True, blank=True)

    class Meta:
        ordering = ('arrived_time',)

class SignDataRequest(BaseSign):
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    notification_url = models.URLField()

    def __str__(self):
        return repr(self)

    def __repr__(self):
        return "SignDataRequest(%d)  %s %r %d %s" % (
            self.id_transaction,
            self.identification,
            self.code,
            self.status,
            self.document_format
        )

    @property
    def left_time(self):
        now = timezone.now()
        ttime = relativedelta(self.expiration_datetime, now)
        return "%d:%d:%d" % (ttime.hours, ttime.minutes, ttime.seconds)

    class Meta:
        ordering = ('request_datetime',)


class SignRequest(BaseInstitutionRequestModel):
    data_request = models.OneToOneField(
        SignDataRequest,
        on_delete=models.CASCADE,
        null=True, blank=True)

    class Meta:
        ordering = ('arrived_time',)


class StampDataRequest(BaseStamp):
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    notification_url = models.URLField()
    eta = models.DateTimeField(null=True, blank=True)
    document = models.TextField(default=' ')
    document_hash = models.TextField(default=' ')
    algorithm_hash = models.CharField(max_length=500, default='Sha256')
    rety_call_bccr = models.SmallIntegerField(default=0)

    def __str__(self):
        return repr(self)

    def __repr__(self):
        return "StampDataRequest(%d)  %d %s -- %s" % (
            self.pk,
            self.status,
            self.document_format,
            self.id_functionality
        )

    @property
    def left_time(self):
        now = timezone.now()
        ttime = relativedelta(self.expiration_datetime, now)
        return "%d:%d:%d" % (ttime.hours, ttime.minutes, ttime.seconds)

    class Meta:
        ordering = ('request_datetime',)


class StampRequest(BaseInstitutionRequestModel):
    data_request = models.OneToOneField(
        StampDataRequest,
        on_delete=models.CASCADE,
        null=True, blank=True)

    class Meta:
        ordering = ('arrived_time',)


class ValidateCertificateDataRequest(BaseValidateCertificate):
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    notification_url = models.URLField()

    def __str__(self):
        return repr(self)

    def __repr__(self):
        return "ValidateCertificateDataRequest(%d)  %s %r %d" % (
            self.id_transaction,
            self.identification,
            self.was_successfully,
            self.status,
        )

    @property
    def id_transaction(self):
        return self.pk

    @property
    def left_time(self):
        now = timezone.now()
        ttime = relativedelta(self.expiration_datetime, now)
        return "%d:%d:%d" % (ttime.hours, ttime.minutes, ttime.seconds)

    class Meta:
        ordering = ('request_datetime',)


class ValidateCertificateRequest(BaseInstitutionRequestModel):
    data_request = models.OneToOneField(
        ValidateCertificateDataRequest,
        on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        ordering = ('arrived_time',)

class ValidateDocumentDataRequest(BaseDocument):
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    notification_url = models.URLField()

    def __str__(self):
        return repr(self)

    def __repr__(self):
        return "ValidateDocumentDataRequest(%d)  %s %r %d" % (
            self.id_transaction,
            self.format,
            self.was_successfully,
            self.status,
        )

    @property
    def id_transaction(self):
        return self.pk

    class Meta:
        ordering = ('request_datetime',)


class ValidateDocumentRequest(BaseInstitutionRequestModel):

    data_request = models.OneToOneField(ValidateDocumentDataRequest,
                                        on_delete=models.CASCADE,
                                        null=True, blank=True)

    class Meta:
        ordering = ('arrived_time',)

