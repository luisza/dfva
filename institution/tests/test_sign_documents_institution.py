'''
Created on 16 ago. 2017

@author: luis
'''
from institution.tests.base_institution_test import SignCase, CheckSignCase
from corebase.test.documents import XMLFILE, HASHXML, ODFFILE, HASHODF, DOCXFILE,\
    HASHDOCX

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