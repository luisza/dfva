'''
Created on 15 ago. 2017

@author: luis
'''

from authenticator.models import AuthenticatePersonDataRequest
from corebase.test.person import BasePersonTest
from corebase.test.institutio_utils import create_institution


class AuthenticatorPersonCase(BasePersonTest):

    def authenticate(self, **kwargs):
        identification = kwargs.get('identification', self.person)
        algorithm = kwargs.get('algorithm', 'sha512')
        response = self.client.authenticate(
            identification, algorithm=algorithm)
        return response

    def test_authenticate(self):
        response = self.authenticate()
        self.ok_test(response)
        self.assertIsNotNone(AuthenticatePersonDataRequest.objects.filter(
            code=response['code']).first())

    def test_algorithms(self):

        for algorithm in ['sha256', 'sha384', 'sha512']:
            response = self.authenticate(algorithm=algorithm)
            self.ok_test(response)

    def test_own_authenticate(self):
        response = self.own_authenticate()
        self.ok_test(response)
        self.assertIsNotNone(AuthenticatePersonDataRequest.objects.filter(
            code=response['code']).first())

    def test_check_wrong_encrypt_authenticate(self):
        """if all credential are well but data is encrypted with other private
        key"""
        institution2 = create_institution(self.user)
#         url = "https://institution2.com/notify"
#         create_url(institution2, url=url)

        def edata_fun(str_data, etype='sign'):
            return self.dummy_encrypt(str_data, institution2.public_key)

        response = self.own_authenticate(
            edata=edata_fun,
            public_certificate=institution2.public_certificate
        )
        self.check_wrong_sign_test(response)
#

    def test_wrong_hashsum(self):
        response = self.own_authenticate(
            hashsum="bd267a725dc16fc0fa33c267af52a25779b8dd628d0df26e5e8813505df8bef05")
        self.wrong_hashsum_test(response)
