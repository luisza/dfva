'''
Created on 15 ago. 2017

@author: luis
'''


from django.utils import timezone

from corebase.test.institution import BaseInstitutionTest
from corebase.rsa import decrypt
import json
from institution.models import AuthenticateDataRequest
from corebase.test.institution_utils import create_url, create_institution
from corebase.test import WRONG_CERTIFICATE



class AuthenticatorInstitutionCase(BaseInstitutionTest):

    def authenticate(self, **kwargs):

        url = kwargs.get('url', self.URL_NOTIFICATION)
        institution = kwargs.get('institution', str(self.institution.code))
        request_datetime = kwargs.get(
            'request_datetime', timezone.now().isoformat())

        data = {
            'institution': institution,
            'notification_url': url,
            'identification': self.IDENTIFICATION,
            'request_datetime': request_datetime,
        }

        params = self.get_request_params(data, **kwargs)

        response = self.client.post('/authenticate/institution/',
                                    params, format='json')
        try:
            response = decrypt(self.institution.private_key,
                               response.data['data'])
        except Exception as e:
            #            print(e)
            try:
                response = json.loads(response.json()['data'])
            except:
                pass

        return response

    def test_authenticate(self):
        response = self.authenticate()
        self.ok_test(response)
        self.assertIsNotNone(AuthenticateDataRequest.objects.filter(
            code=response['code']).first())

    def test_algorithms(self):

        for algorithm in ['sha256', 'sha384', 'sha512']:
            response = self.authenticate(algorithm=algorithm)
            self.ok_test(response)

    def test_check_wrong_url(self):
        response = self.authenticate(url='https://dfva.cr/ups')
        self.check_wrong_url_test(response)

    def test_check_wrong_institution(self):
        response = self.authenticate(institution='no institution')
        self.check_wrong_institution_test(response)

    def test_check_wrong_sign(self):
        """if all credential are well but data is encrypted with other private
        key"""
        institution2 = create_institution(self.user)
        url = "https://institution2.com/notify"
        create_url(institution2, url=url)

        response = self.authenticate(institution=str(institution2.code),
                                     url=url,
                                     public_certificate=institution2.public_certificate)

        response = decrypt(institution2.private_key,
                           response.data['data'])

        self.check_wrong_sign_test(response)

    def test_wrong_hashsum(self):
        response = self.authenticate(
            hashsum="bd267a725dc16fc0fa33c267af52a25779b8dd628d0df26e5e8813505df8bef05")
        self.wrong_hashsum_test(response)

    def test_wrong_certificate(self):

        response = self.authenticate(
            public_certificate=WRONG_CERTIFICATE
        )
        self.wrong_certificate_test(response)
