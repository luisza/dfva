from validator.tests.base_institution_test import BaseValidateInstitutionCase
from validator.models import ValidateCertificateDataRequest,\
    ValidateDocumentDataRequest
from validator.tests.certificate import CERTIFICATE_FILE


class ValidateCertificateInstitution(BaseValidateInstitutionCase):
    REQUEST_URL = '/validate/institution_certificate/'
    DATAREQUEST = ValidateCertificateDataRequest
    DOCUMENT = CERTIFICATE_FILE


class ValidateDocumentInstitution(BaseValidateInstitutionCase):
    REQUEST_URL = '/validate/institution_document/'
    DATAREQUEST = ValidateDocumentDataRequest
    DOCUMENT = CERTIFICATE_FILE