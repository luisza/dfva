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
    FORMAT='cofirma'
    
class ValidateDocumentContrafirmaInstitution(BaseValidateInstitutionCase):
    REQUEST_URL = '/validate/institution_document/'
    DATAREQUEST = ValidateDocumentDataRequest
    DOCUMENT = CERTIFICATE_FILE
    FORMAT='contrafirma'
    
class ValidateDocumentMSOfficeInstitution(BaseValidateInstitutionCase):
    REQUEST_URL = '/validate/institution_document/'
    DATAREQUEST = ValidateDocumentDataRequest
    DOCUMENT = CERTIFICATE_FILE
    FORMAT='msoffice'
    
class ValidateDocumentODFInstitution(BaseValidateInstitutionCase):
    REQUEST_URL = '/validate/institution_document/'
    DATAREQUEST = ValidateDocumentDataRequest
    DOCUMENT = CERTIFICATE_FILE
    FORMAT='odf'