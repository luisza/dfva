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
@date: 16/8/2017
@author: Universidad de Costa Rica
@maintainer: Luis Zarate Montero
@contact: luis.zarate@solvosoft.com
@license: GPLv3
'''

from institution.tests.base_institution_test import BaseValidateInstitutionCase
from institution.models import ValidateCertificateDataRequest,\
    ValidateDocumentDataRequest
from corebase.test import CERTIFICATE_FILE


class ValidateCertificateInstitution(BaseValidateInstitutionCase):
    REQUEST_URL = '/validate/institution_certificate/'
    DATAREQUEST = ValidateCertificateDataRequest
    DOCUMENT = CERTIFICATE_FILE


class ValidateDocumentCofirmaInstitution(BaseValidateInstitutionCase):
    REQUEST_URL = '/validate/institution_document/'
    DATAREQUEST = ValidateDocumentDataRequest
    DOCUMENT = CERTIFICATE_FILE
    FORMAT = 'cofirma'


class ValidateDocumentContrafirmaInstitution(BaseValidateInstitutionCase):
    REQUEST_URL = '/validate/institution_document/'
    DATAREQUEST = ValidateDocumentDataRequest
    DOCUMENT = CERTIFICATE_FILE
    FORMAT = 'contrafirma'


class ValidateDocumentMSOfficeInstitution(BaseValidateInstitutionCase):
    REQUEST_URL = '/validate/institution_document/'
    DATAREQUEST = ValidateDocumentDataRequest
    DOCUMENT = CERTIFICATE_FILE
    FORMAT = 'msoffice'


class ValidateDocumentODFInstitution(BaseValidateInstitutionCase):
    REQUEST_URL = '/validate/institution_document/'
    DATAREQUEST = ValidateDocumentDataRequest
    DOCUMENT = CERTIFICATE_FILE
    FORMAT = 'odf'
