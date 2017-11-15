'''
Created on 16 ago. 2017

@author: luis
'''
from institution.tests.base_institution_test import SignCase, CheckSignCase,\
    DeleteSignCase
from corebase.test.documents import XMLFILE, HASHXML, ODFFILE, HASHODF, DOCXFILE,\
    HASHDOCX


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