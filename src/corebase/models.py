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

from django.db import models
from django.core.validators import RegexValidator
import uuid
from django.contrib.auth.models import User
from django.utils.translation import gettext as _
from pyfva import constants


identification_validator = RegexValidator(
    r'(^[1|5]\d{11}$)|(^\d{2}-\d{4}-\d{4}$)',
    message=_("Debe tener el formato 08-8888-8888 para nacionales o 500000000000 o 100000000000"))

ALGORITHM = (
    ('sha256', 'sha256'),
    ('sha384', 'sha384'),
    ('sha512', 'sha512')
)

SUPPORTED_DOC_FORMAT = ['xml_cofirma',
                        'xml_contrafirma', 'odf', 'msoffice', 'pdf']


class BaseRequestModel(models.Model):
    code = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    arrived_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    data_hash = models.CharField(max_length=130,
                                 help_text=_("""Suma hash de datos de tamaño máximo 130 caracteres, usando el
                                 algoritmo especificado """))
    algorithm = models.CharField(max_length=7, choices=ALGORITHM,
                                 help_text=_(""" Debe ser alguno de los siguientes: sha256, sha384, sha512"""))

    class Meta:
        abstract = True


class BaseAuthenticate(models.Model):
    arrived_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    identification = models.CharField(
        max_length=15, validators=[identification_validator],
        help_text=_("Debe tener el formato 08-8888-8888 para nacionales o 500000000000 o 100000000000")
    )
    # '%Y-%m-%d %H:%M:%S',   es decir  '2006-10-25 14:30:59'
    request_datetime = models.DateTimeField(
        help_text=_("""'%Y-%m-%d %H:%M:%S',   es decir  '2006-10-25 14:30:59'"""))
    code = models.CharField(max_length=20, default='N/D')
    status = models.IntegerField(
        default=0, choices=constants.ERRORES_AL_SOLICITAR_FIRMA)
    status_text = models.CharField(max_length=256, default='n/d')
    sign_document = models.TextField(null=True, blank=True)
    response_datetime = models.DateTimeField(auto_now=True)
    expiration_datetime = models.DateTimeField()
    id_transaction = models.IntegerField(default=0, db_index=True)
    duration = models.SmallIntegerField(default=3)
    received_notification = models.BooleanField(default=False)
    resume = models.CharField(max_length=250, null=True, blank=True)
    hash_docsigned = models.TextField(null=True, blank=True)
    hash_id_docsigned = models.SmallIntegerField(default=0)

    class Meta:
        abstract = True


class BaseSign(BaseAuthenticate):
    document_format = models.CharField(max_length=25, default='n/d')
    place = models.CharField(max_length=150, null=True, blank=True)
    reason = models.CharField(max_length=125, null=True, blank=True)

    class Meta:
        abstract = True

class BaseValidateCertificate(models.Model):
    arrived_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    identification = models.CharField(
        max_length=15, null=True, validators=[identification_validator],
        help_text=_("Debe tener el formato 08-8888-8888 para nacionales o 500000000000 o 100000000000")
    )
    # '%Y-%m-%d %H:%M:%S',   es decir  '2006-10-25 14:30:59'
    request_datetime = models.DateTimeField(
        help_text=_("""'%Y-%m-%d %H:%M:%S',   es decir  '2006-10-25 14:30:59'"""))
    code = models.CharField(max_length=20, default='N/D')
    status = models.IntegerField(
        choices=constants.ERRORES_VALIDA_CERTIFICADO, default=0)
    status_text = models.CharField(max_length=256, default='n/d')
    response_datetime = models.DateTimeField(auto_now=True)
    was_successfully = models.BooleanField(default=True)
    full_name = models.CharField(max_length=250, null=True)
    start_validity = models.DateTimeField(null=True)
    end_validity = models.DateTimeField(null=True)

    class Meta:
        abstract = True



class WarningReceived(models.Model):
    description = models.CharField(max_length=512)

    def __str__(self):
        return self.description


class ErrorFound(models.Model):
    code = models.CharField(max_length=250)
    detail = models.TextField()

    def __str__(self):
        return self.code


class Signer(models.Model):
    identification_number = models.CharField(max_length=25)
    signature_date = models.DateField()
    full_name = models.CharField(max_length=25)

    def __str__(self):
        return self.full_name


class BaseDocument(models.Model):
    FORMATS = (
        ('cofirma', 'CoFirma'),
        ('contrafirma', 'ContraFirma'),
        ('msoffice', 'MS Office'),
        ('odf', 'Open Document Format'),
        ('pdf', 'PDF')
    )
    warnings = models.ManyToManyField(WarningReceived)
    errors = models.ManyToManyField(ErrorFound)
    signers = models.ManyToManyField(Signer)
    request_datetime = models.DateTimeField()
    code = models.CharField(max_length=20, default='N/D')
    format = models.CharField(max_length=15, default='n/d', choices=FORMATS)
    status = models.IntegerField(default=0)
    status_text = models.CharField(max_length=256, default='n/d')
    was_successfully = models.BooleanField(default=True)
    arrived_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    def get_status_display(self):
        keys = {}
        if format == 'cofirma':
            keys = dict(constants.ERRORES_VALIDAR_XMLCOFIRMA)
        elif format == 'contrafirma':
            keys = dict(constants.ERRORES_VALIDAR_XMLCONTRAFIRMA)
        elif format == 'msoffice':
            keys = dict(constants.ERRORES_VALIDAR_MSOFFICE)
        elif format == 'odf':
            keys = dict(constants.ERRORES_VALIDAR_ODF)
        elif format == 'pdf':
            keys = dict(constants.ERRORES_VALIDAR_PDF)
        if self.status in keys:
            return keys[self.status]
        return _("No code reference %d") % (self.status,)

    class Meta:
        abstract = True
