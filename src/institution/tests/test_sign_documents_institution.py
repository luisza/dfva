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

from institution.tests.base_institution_test import SignCase, CheckSignCase,\
    DeleteSignCase
from corebase.test.documents import XMLFILE, HASHXML, ODFFILE, HASHODF, \
    DOCXFILE, HASHDOCX, HASHPDF, PDFFILE


# ---- Sign -------
class SignXmlCoFirmaCase(SignCase):
    DOCUMENT = XMLFILE
    HASH = HASHXML
    FORMAT = 'xml_cofirma'


class SignXmlContraFirmaCase(SignCase):
    DOCUMENT = XMLFILE
    HASH = HASHXML
    FORMAT = 'xml_contrafirma'


class SignODFCase(SignCase):
    DOCUMENT = ODFFILE
    HASH = HASHODF
    FORMAT = 'odf'


class SignMSOfficeCase(SignCase):
    DOCUMENT = DOCXFILE
    HASH = HASHDOCX
    FORMAT = 'msoffice'

class SignPDFCase(SignCase):
    DOCUMENT = PDFFILE
    HASH = HASHPDF
    FORMAT = 'pdf'

    def test_wrong_reason_size(self):
        response = self.sign(reason="a"*126)
        self.assertEqual(response['status'], 8)

    def test_wrong_reason_size(self):
        response = self.sign(place="a"*151)
        self.assertEqual(response['status'], 11)


# --------- Check sign ---------


class CheckSignXmlCoFirmaCase(CheckSignCase):
    DOCUMENT = XMLFILE
    HASH = HASHXML
    FORMAT = 'xml_cofirma'


class CheckSignXmlContraFirmaCase(CheckSignCase):
    DOCUMENT = XMLFILE
    HASH = HASHXML
    FORMAT = 'xml_contrafirma'


class CheckSignODFCase(CheckSignCase):
    DOCUMENT = ODFFILE
    HASH = HASHODF
    FORMAT = 'odf'


class CheckSignMSOfficeCase(CheckSignCase):
    DOCUMENT = DOCXFILE
    HASH = HASHDOCX
    FORMAT = 'msoffice'

class CheckSignPDFCase(CheckSignCase):
    DOCUMENT = PDFFILE
    HASH = HASHPDF
    FORMAT = 'pdf'
    REASON = "Una prueba"
    PLACE = "Un lugar de la mancha"

# ----- DELETE -----------------


class DeleteSignXmlCoFirmaCase(DeleteSignCase):
    DOCUMENT = XMLFILE
    HASH = HASHXML
    FORMAT = 'xml_cofirma'


class DeleteSignXmlContraFirmaCase(DeleteSignCase):
    DOCUMENT = XMLFILE
    HASH = HASHXML
    FORMAT = 'xml_contrafirma'


class DeleteSignODFCase(DeleteSignCase):
    DOCUMENT = ODFFILE
    HASH = HASHODF
    FORMAT = 'odf'


class DeleteSignMSOfficeCase(DeleteSignCase):
    DOCUMENT = DOCXFILE
    HASH = HASHDOCX
    FORMAT = 'msoffice'

class DeleteSignPDFCase(DeleteSignCase):
    DOCUMENT = PDFFILE
    HASH = HASHPDF
    FORMAT = 'pdf'
    REASON = "Una prueba"
    PLACE = "Un lugar de la mancha"
