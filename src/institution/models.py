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
    BaseRequestModel, BaseAuthenticate, BaseSign, BaseValidateCertificate
from institution.presentation import PEMpresentation
from django.contrib.auth.models import User
import uuid
from django.conf import settings
from corebase.rsa import salt_decrypt, salt_encrypt
from asn1crypto import pem,  x509
from dateutil.parser import parse
from pyfva import constants


class EncrytedText(models.TextField):

    def from_db_value(self, value, expression, connection, context):
        return salt_decrypt(value)

    def pre_save(self, model_instance, add):
        return salt_encrypt(getattr(model_instance, self.attname))


class Institution(models.Model, PEMpresentation):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=250)
    code = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    active = models.BooleanField(default=True)
    bccr_bussiness = models.IntegerField(default=settings.DEFAULT_BUSSINESS)
    bccr_entity = models.IntegerField(default=settings.DEFAULT_ENTITY)

    domain = models.CharField(max_length=250)  # Certificate domain
    institution_unit = models.CharField(
        max_length=250, default="ND")  # UO in cert
    private_key = models.TextField()
    public_key = EncrytedText()
    public_certificate = EncrytedText()
    server_sign_key = EncrytedText()
    server_public_key = EncrytedText()

    email = models.EmailField()
    phone = models.CharField(max_length=25, null=True, blank=False)
    administrative_institution = models.BooleanField(default=False)

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
        permissions = (
            ("view_institution", "Can see available tasks"),
        )


class NotificationURL(models.Model):
    description = models.CharField(max_length=250)
    url = models.URLField(null=True, blank=True)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    not_webapp = models.BooleanField(default=False)
    is_demo = models.BooleanField(default=False)

    def __str__(self):
        return "%s %s" % (
            self.institution.name,
            self.url or 'N/D'
        )

    class Meta:
        ordering = ('institution',)
        permissions = (
            ("view_notificationurl", "Can see available notification urls"),
        )


class InstitutionStats(models.Model):
    institution = models.ForeignKey(Institution)
    datetime = models.DateTimeField(auto_now_add=True)
    status = models.SmallIntegerField(default=1)
    notified = models.BooleanField(default=False)
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
    institution = models.ForeignKey(Institution)
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
        permissions = (
            ("view_authenticatedatarequest",
             "Can see available Authenticate Data Request"),
        )


class AuthenticateRequest(BaseInstitutionRequestModel):
    data_request = models.OneToOneField(
        AuthenticateDataRequest,
        on_delete=models.CASCADE,
        null=True, blank=True)

    class Meta:
        ordering = ('arrived_time',)
        permissions = (
            ("view_authenticaterequest", "Can see available Authenticate Request"),
        )


class SignDataRequest(BaseSign):
    institution = models.ForeignKey(Institution)
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
        permissions = (
            ("view_signerdatarequest",
             "Can see available Signer Data Request"),
        )


class SignRequest(BaseInstitutionRequestModel):
    data_request = models.OneToOneField(
        SignDataRequest,
        on_delete=models.CASCADE,
        null=True, blank=True)

    class Meta:
        ordering = ('arrived_time',)
        permissions = (
            ("view_signrequest", "Can see available Sign Request"),
        )


class ValidateCertificateDataRequest(BaseValidateCertificate):
    institution = models.ForeignKey(Institution)
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
        permissions = (
            ("view_validatecertificatedatarequest",
             "Can see available validate certificate Data Request"),
        )


class ValidateCertificateRequest(BaseInstitutionRequestModel):
    data_request = models.OneToOneField(
        ValidateCertificateDataRequest,
        on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        ordering = ('arrived_time',)
        permissions = (
            ("view_validaterequest", "Can see available validate certificate Request"),
        )


class ValidateDocumentDataRequest(BaseDocument):
    FORMATS = (
        ('cofirma', 'CoFirma'),
        ('contrafirma', 'ContraFirma'),
        ('msoffice', 'MS Office'),
        ('odf', 'Open Document Format'),
        ('pdf', 'PDF')
    )
    institution = models.ForeignKey(Institution)
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
        permissions = (
            ("view_validatedocumentdatarequest",
             "Can see available validate document Data Request"),
        )


class ValidateDocumentRequest(BaseInstitutionRequestModel):

    data_request = models.OneToOneField(ValidateDocumentDataRequest,
                                        on_delete=models.CASCADE,
                                        null=True, blank=True)

    class Meta:
        ordering = ('arrived_time',)
        permissions = (
            ("view_validatedocumentrequest",
             "Can see validate document Sign Request"),
        )
