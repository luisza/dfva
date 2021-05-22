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
from django.core.serializers.json import DjangoJSONEncoder
from django.db import models
from django.utils import timezone
from corebase.models import identification_validator,\
    BaseDocument, BaseRequestModel, ALGORITHM
from django.contrib.auth.models import User
from django.conf import settings

class Person(models.Model):
    ERROR_CODE = (
        (1, 'Transacción satisfactoria'),
        (2, 'Error, persona no existe'),
        (3, 'Error no determinado')

    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    identification = models.CharField(max_length=20, primary_key=True)
    expiration_datetime_token = models.DateTimeField(null=True, blank=True)
    last_error_code = models.SmallIntegerField(default=1, choices=ERROR_CODE)
    authenticate_certificate = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.user.get_full_name() or self.identification


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


def get_default_expiration():
    return timezone.now()+relativedelta(minutes=settings.EXPIRED_DELTA)

class TransactionData(models.Model):
    request_datetime = models.DateTimeField()
    code = models.CharField(max_length=20, default='N/D')
    STATUS = ((0, 'Solicitud recibida correctamente'),
              (1, 'Ha ocurrido algún problema al solicitar la firma'),
              (2, 'Solicitud con campos incompletos'),
              (3, 'Diferencia de hora no permitida entre cliente y servidor'),
              (4, 'La entidad no se encuentra registrada'),
              (5, 'La entidad se encuentra en estado inactiva'),
              (6, 'La URL no pertenece a la entidad solicitante'),
              (7, 'El tamaño de hash debe ser entre 1 y 130 caracteres'),
              (8, 'Algoritmo desconocido'),
              (9, 'Certificado incorrecto'))
    status = models.IntegerField(choices=STATUS, default=0)
    status_text = models.CharField(max_length=256, default='n/d')
    response_datetime = models.DateTimeField(auto_now=True)
    expiration_datetime = models.DateTimeField(default=get_default_expiration)

    @property
    def left_time(self):
        now = timezone.now()
        ttime = relativedelta(self.expiration_datetime, now)
        return "%d:%d:%d" % (ttime.hours, ttime.minutes, ttime.seconds)

    class Meta:
        abstract = True


class BaseBasePersonRequest(TransactionData):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    identification = models.CharField(
        max_length=15, validators=[identification_validator],
        help_text="""'%Y-%m-%d %H:%M:%S',   es decir  '2006-10-25 14:30:59'""")
    # '%Y-%m-%d %H:%M:%S',   es decir  '2006-10-25 14:30:59'


    class Meta:
        abstract = True


class BasePersonRequest(BaseBasePersonRequest):

    id_transaction = models.IntegerField(default=0)
    signed_document = models.TextField(null=True, blank=True)
    duration = models.SmallIntegerField(default=3)
    received_notification = models.BooleanField(default=False)
    hash_docsigned = models.TextField(null=True, blank=True)
    hash_id_docsigned = models.SmallIntegerField(default=0)

    class Meta:
        abstract = True


class AuthenticatePersonRequest(BasePersonRequest):
    arrived_time = models.DateTimeField(auto_now_add=True)
    public_certificate = models.TextField(help_text="""Certificado público  de firma, para firma digital avanzada""")
    document_hash = models.TextField()
    resume = models.CharField(max_length=500)

    class Meta:
        ordering = ('arrived_time',)


class SignPersonRequest(BasePersonRequest):
    arrived_time = models.DateTimeField(auto_now_add=True)
    document = models.TextField()
    format = models.CharField(max_length=15)
    algorithm_hash = models.CharField(max_length=50)
    document_hash = models.TextField()
    resume = models.CharField(max_length=500)
    public_certificate = models.TextField(help_text="""Certificado público  de firma, para firma digital avanzada""")
    place = models.CharField(max_length=256, null=True, blank=True)
    reason = models.CharField(max_length=256, null=True, blank=True)

    class Meta:
        ordering = ('arrived_time',)


class ValidatePersonDocumentRequest(models.Model):
    FORMATS = (
        ('cofirma', 'CoFirma'),
        ('contrafirma', 'ContraFirma'),
        ('msoffice', 'MS Office'),
        ('odf', 'Open Document Format'),
        ('pdf', 'PDF')
    )
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    document = models.TextField()
    response_datetime = models.DateTimeField()
    validation_data = models.JSONField(null=True, blank=True, encoder=DjangoJSONEncoder)
    #: Formato del documento a validar
    format = models.CharField(max_length=15, default='n/d', choices=FORMATS)
    #: Hora en la que se recibió la petición por parte del usuario
    request_datetime = models.DateTimeField()
    status = models.IntegerField(default=0)
    #: Traduce el código del status para ser leido por personas
    status_text = models.CharField(max_length=256, default='n/d')
    #: El documento es válido
    was_successfully = models.BooleanField(default=True)
    #: Hora en la que se recibe la solicitud de validación (metricas)
    arrived_time = models.DateTimeField(auto_now_add=True)
    #: Hora en la que se recibe la respuesta de la validación por parte del BCCR
    update_time = models.DateTimeField(auto_now=True)

    @property
    def id_transaction(self):
        return self.pk

    class Meta:
        ordering = ('arrived_time',)


class ValidatePersonCertificateRequest(TransactionData, models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    identification = models.CharField(
        max_length=15, null=True, blank=True,
        help_text="""'%Y-%m-%d %H:%M:%S',   es decir  '2006-10-25 14:30:59'""")
    # '%Y-%m-%d %H:%M:%S',   es decir  '2006-10-25 14:30:59'

    arrived_time = models.DateTimeField(auto_now_add=True)
    was_successfully = models.BooleanField(default=True)
    full_name = models.CharField(max_length=250, null=True)
    start_validity = models.DateTimeField(null=True)
    end_validity = models.DateTimeField(null=True)
    document = models.TextField()
    format = models.CharField(max_length=20)

    @property
    def id_transaction(self):
        return self.pk

    class Meta:
        ordering = ('arrived_time',)

