'''
Created on 20 ago. 2017

@author: luis
'''
from validator.tests.certificate import CERTIFICATE_FILE
from validator.models import ValidatePersonCertificateDataRequest,\
    ValidatePersonDocumentDataRequest
from validator.tests.base_person_test import BaseValidatePersonCase


class ValidateCertificatePerson(BaseValidatePersonCase):
    REQUEST_URL = '/validate/person_certificate/'
    DATAREQUEST = ValidatePersonCertificateDataRequest
    DOCUMENT = CERTIFICATE_FILE


class ValidateDocumentPerson(BaseValidatePersonCase):
    REQUEST_URL = '/validate/person_document/'
    DATAREQUEST = ValidatePersonDocumentDataRequest
    DOCUMENT = CERTIFICATE_FILE
