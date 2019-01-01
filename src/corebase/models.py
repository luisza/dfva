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
    warnings = models.ManyToManyField(WarningReceived)
    errors = models.ManyToManyField(ErrorFound)
    signers = models.ManyToManyField(Signer)
