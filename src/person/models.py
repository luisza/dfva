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
@author: Luis Zarate Montero
@contact: luis.zarate@solvosoft.com
@license: GPLv3
'''

from dateutil.relativedelta import relativedelta
from django.db import models
from django.utils import timezone
from corebase.models import identification_validator, \
    BaseDocument, BaseRequestModel, ALGORITHM, BaseAuthenticate, BaseSign, BaseValidateCertificate
from django.contrib.auth.models import User


class Person(models.Model):
    ERROR_CODE = (
        (1, 'Transacción satisfactoria'),
        (2, 'Error, persona no existe'),
        (3, 'Error no determinado')

    )
    user = models.OneToOneField(User)
    identification = models.CharField(max_length=20, primary_key=True)
    token = models.TextField(null=True, blank=True)
    cipher_token = models.TextField(null=True, blank=True)
    expiration_datetime_token = models.DateTimeField(null=True, blank=True)
    last_error_code = models.SmallIntegerField(default=1, choices=ERROR_CODE)
    authenticate_certificate = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.user.get_full_name() or self.identification


class BasePersonRequestModel(BaseRequestModel):
    public_certificate = models.TextField(
        help_text="""Certificado público  de firma, para firma digital avanzada""")
    person = models.CharField(
        max_length=50, help_text="Identificación de la persona solicitante")

    class Meta:
        abstract = True


class PersonLogin(models.Model):
    arrived_time = models.DateTimeField(auto_now_add=True)
    public_certificate = models.TextField(
        help_text="""Certificado público  de firma, para firma digital avanzada""")
    code = models.TextField()
    person = models.CharField(
        max_length=50, help_text="Identificación de la persona solicitante")
    data_hash = models.CharField(max_length=130,
                                 help_text="""Suma hash de datos de tamaño máximo 130 caracteres, usando el
                                 algoritmo especificado """)
    algorithm = models.CharField(max_length=7, choices=ALGORITHM,
                                 help_text=""" Debe ser alguno de los siguientes: sha256, sha384, sha512""")

    def __str__(self):
        return self.person


class AuthenticatePersonDataRequest(BaseAuthenticate):
    person = models.ForeignKey(Person)

    @property
    def left_time(self):
        now = timezone.now()
        ttime = relativedelta(self.expiration_datetime, now)
        return "%d:%d:%d" % (ttime.hours, ttime.minutes, ttime.seconds)

    class Meta:
        ordering = ('request_datetime',)
        permissions = (
            ("view_authenticatepersondatarequest",
             "Can see available Authenticate Person Data Request"),
        )


class AuthenticatePersonRequest(BasePersonRequestModel):
    data_request = models.OneToOneField(AuthenticatePersonDataRequest,
                                        on_delete=models.CASCADE,
                                        null=True, blank=True)

    class Meta:
        ordering = ('arrived_time',)
        permissions = (
            ("view_authenticatepersonrequest",
             "Can see available Authenticate Person Request"),
        )


class SignPersonDataRequest(BaseSign):
    person = models.ForeignKey(Person)

    @property
    def left_time(self):
        now = timezone.now()
        ttime = relativedelta(self.expiration_datetime, now)
        return "%d:%d:%d" % (ttime.hours, ttime.minutes, ttime.seconds)

    class Meta:
        ordering = ('request_datetime',)
        permissions = (
            ("view_signerdatarequest",
             "Can see available Signer Person Data Request"),
        )


class SignPersonRequest(BasePersonRequestModel):
    data_request = models.OneToOneField(
        SignPersonDataRequest,
        on_delete=models.CASCADE,
        null=True, blank=True)

    class Meta:
        ordering = ('arrived_time',)
        permissions = (
            ("view_signpersonrequest", "Can see available Person Sign Request"),
        )


class ValidatePersonCertificateDataRequest(BaseValidateCertificate):
    person = models.ForeignKey(Person)

    class Meta:
        ordering = ('request_datetime',)
        permissions = (
            ("view_validatePersoncertificatedatarequest",
             "Can see available validate Person certificate Data Request"),
        )


class ValidatePersonDocumentDataRequest(BaseDocument):
    person = models.ForeignKey(Person)

    @property
    def id_transaction(self):
        return self.pk

    class Meta:
        ordering = ('request_datetime',)
        permissions = (
            ("view_validatepersondocumentdatarequest",
             "Can see available validate document Data Request"),
        )


class ValidatePersonDocumentRequest(BasePersonRequestModel):
    data_request = models.OneToOneField(
        ValidatePersonDocumentDataRequest,
        on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        ordering = ('arrived_time',)
        permissions = (
            ("view_validatepersondocumentrequest",
             "Can see validate document Sign Request"),
        )


class ValidatePersonCertificateRequest(BasePersonRequestModel):

    data_request = models.OneToOneField(
        ValidatePersonCertificateDataRequest,
        on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        ordering = ('arrived_time',)
        permissions = (
            ("view_validatePersonrequest",
             "Can see available validate certificate Request"),
        )
