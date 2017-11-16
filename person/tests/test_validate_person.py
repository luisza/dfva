'''
Created on 20 ago. 2017

@author: luis
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
    FORMAT='cofirma'

class ValidateDocumentContraFirmaPerson(BaseValidatePersonCase):
    REQUEST_URL = '/validate/person_document/'
    DATAREQUEST = ValidatePersonDocumentDataRequest
    DOCUMENT = CERTIFICATE_FILE
    FORMAT='contrafirma'
    
class ValidateDocumentMSOfficePerson(BaseValidatePersonCase):
    REQUEST_URL = '/validate/person_document/'
    DATAREQUEST = ValidatePersonDocumentDataRequest
    DOCUMENT = CERTIFICATE_FILE
    FORMAT='msoffice'

class ValidateDocumentODFPerson(BaseValidatePersonCase):
    REQUEST_URL = '/validate/person_document/'
    DATAREQUEST = ValidatePersonDocumentDataRequest
    DOCUMENT = CERTIFICATE_FILE
    FORMAT='odf'