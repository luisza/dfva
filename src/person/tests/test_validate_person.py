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
@date: 20/8/2017
@author: Luis Zarate Montero
@contact: luis.zarate@solvosoft.com
@license: GPLv3
'''

from person.tests.base_person_test import BaseValidatePersonCase
from person.models import ValidatePersonCertificateDataRequest,\
    ValidatePersonDocumentDataRequest
from corebase.test import CERTIFICATE_FILE


class ValidateCertificatePerson(BaseValidatePersonCase):
    REQUEST_URL = '/validate/person_certificate/'
    DATAREQUEST = ValidatePersonCertificateDataRequest
    DOCUMENT = CERTIFICATE_FILE


class ValidateDocumentCoFirmaPerson(BaseValidatePersonCase):
    REQUEST_URL = '/validate/person_document/'
    DATAREQUEST = ValidatePersonDocumentDataRequest
    DOCUMENT = CERTIFICATE_FILE
    FORMAT = 'cofirma'


class ValidateDocumentContraFirmaPerson(BaseValidatePersonCase):
    REQUEST_URL = '/validate/person_document/'
    DATAREQUEST = ValidatePersonDocumentDataRequest
    DOCUMENT = CERTIFICATE_FILE
    FORMAT = 'contrafirma'


class ValidateDocumentMSOfficePerson(BaseValidatePersonCase):
    REQUEST_URL = '/validate/person_document/'
    DATAREQUEST = ValidatePersonDocumentDataRequest
    DOCUMENT = CERTIFICATE_FILE
    FORMAT = 'msoffice'


class ValidateDocumentODFPerson(BaseValidatePersonCase):
    REQUEST_URL = '/validate/person_document/'
    DATAREQUEST = ValidatePersonDocumentDataRequest
    DOCUMENT = CERTIFICATE_FILE
    FORMAT = 'odf'
