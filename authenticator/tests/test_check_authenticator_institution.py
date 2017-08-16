'''
Created on 16 ago. 2017

@author: luis
'''
'''
Created on 15 ago. 2017

@author: luis
'''

from corebase.test.institutio_utils import create_institution, create_url
from django.utils import timezone


from authenticator.models import AuthenticateDataRequest
from authenticator.tests import WRONG_CERTIFICATE
from corebase.test.institution import BaseInstitutionTest


class CheckAuthenticatorInstitutionCase(BaseInstitutionTest):
    BASE_URL = '/authenticate/%s/institution_show/'

    def setUp(self):
        super(CheckAuthenticatorInstitutionCase, self).setUp()
        response = self.authenticate()
        self.data = response.data

    def authenticate(self, **kwargs):

        url = kwargs.get('url', self.URL_NOTIFICATION)
        institution = kwargs.get('institution', str(self.institution.code))
        request_datetime = kwargs.get(
            'request_datetime', timezone.now().isoformat())

        request_url = kwargs.get('request_url', '/authenticate/institution/')
        data = {
            'institution': institution,
            'notification_url': url,
            'identification': self.IDENTIFICATION,
            'request_datetime': request_datetime,
        }

        params = self.get_request_params(data, **kwargs)

        response = self.client.post(request_url,
                                    params, format='json')
        return response

    def test_authenticate_check(self):
        response = self.authenticate()
        self.ok_test(response)
        self.assertIsNotNone(AuthenticateDataRequest.objects.filter(
            code=response.data['code']).first())

        response = self.authenticate(
            request_url=self.BASE_URL % (response.data['code'],))
        self.ok_test(response)

    def test_algorithms(self):

        for algorithm in ['sha256', 'sha384', 'sha512']:
            response = self.authenticate(algorithm=algorithm)
            response = self.authenticate(
                algorithm=algorithm,
                request_url=self.BASE_URL % (response.data['code'],))
            self.ok_test(response)

    def test_check_wrong_url(self):
        response = self.authenticate(
            url='https://dfva.cr/ups',
            request_url=self.BASE_URL % (self.data['code'],))
        self.check_wrong_url_test(response)

    def test_check_wrong_institution(self):
        response = self.authenticate(
            institution='no institution',
            request_url=self.BASE_URL % (self.data['code'],)
        )
        self.check_wrong_institution_test(response)

    def test_check_wrong_sign(self):
        """if all credential are well but data is encrypted with other private
        key"""
        institution2 = create_institution(self.user)
        url = "https://institution2.com/notify"
        create_url(institution2, url=url)

        response = self.authenticate(institution=str(institution2.code),
                                     url=url,
                                     public_certificate=institution2.public_certificate,
                                     request_url=self.BASE_URL % (
                                         self.data['code'],)
                                     )
        self.check_wrong_sign_test(response)

    def test_wrong_hashsum(self):
        response = self.authenticate(request_url=self.BASE_URL % (
            self.data['code'],),
            hashsum="bd267a725dc16fc0fa33c267af52a25779b8dd628d0df26e5e8813505df8bef05")
        self.wrong_hashsum_test(response)

    def test_wrong_certificate(self):

        response = self.authenticate(request_url=self.BASE_URL % (
            self.data['code'],),
            public_certificate=WRONG_CERTIFICATE
        )
        self.wrong_certificate_test(response)
