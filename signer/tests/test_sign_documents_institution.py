'''
Created on 16 ago. 2017

@author: luis
'''

from signer.tests.xmlfile import XMLFILE, HASHXML
from signer.tests.base_institution_test import SignCase, CheckSignCase
from signer.tests.odffile import ODFFILE, HASHODF
from signer.tests.docxfile import DOCXFILE, HASHDOCX


class SignXmlCase(SignCase):
    DOCUMENT = XMLFILE
    HASH = HASHXML
    FORMAT = 'xml'


class SignODFCase(SignCase):
    DOCUMENT = ODFFILE
    HASH = HASHODF
    FORMAT = 'odf'


class SignMSOfficeCase(SignCase):
    DOCUMENT = DOCXFILE
    HASH = HASHDOCX
    FORMAT = 'msoffice'


class CheckSignXmlCase(CheckSignCase):
    DOCUMENT = XMLFILE
    HASH = HASHXML
    FORMAT = 'xml'


class CheckSignODFCase(CheckSignCase):
    DOCUMENT = ODFFILE
    HASH = HASHODF
    FORMAT = 'odf'


class CheckSignMSOfficeCase(CheckSignCase):
    DOCUMENT = DOCXFILE
    HASH = HASHDOCX
    FORMAT = 'msoffice'