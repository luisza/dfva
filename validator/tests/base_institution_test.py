'''
Created on 16 ago. 2017

@author: luis
'''
from corebase.test.institution import BaseInstitutionTest
from django.utils import timezone
from authenticator.tests import WRONG_CERTIFICATE
from corebase.test.institutio_utils import create_institution, create_url
import json
from corebase.rsa import decrypt


class BaseValidateInstitutionCase(BaseInstitutionTest):
    REQUEST_URL = None
    DATAREQUEST = None

    def validate(self, **kwargs):
        url = kwargs.get('url', self.URL_NOTIFICATION)
        institution = kwargs.get('institution', str(self.institution.code))
        request_datetime = kwargs.get(
            'request_datetime', timezone.now().isoformat())
        certificate = kwargs.get('certificate', self.DOCUMENT)
        request_url = kwargs.get(
            'request_url', self.REQUEST_URL)
        data = {
            'institution': institution,
            'notification_url': url,
            'document': certificate,
            'request_datetime': request_datetime,
        }

        params = self.get_request_params(data, **kwargs)

        response = self.client.post(request_url,
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

    def test_sign(self):
        if self.REQUEST_URL is None:
            return
        response = self.validate()
        self.ok_test(response)
        self.assertIsNotNone(self.DATAREQUEST.objects.filter(
            code=response['code']).first())

    def test_algorithms(self):
        if self.REQUEST_URL is None:
            return
        for algorithm in ['sha256', 'sha384', 'sha512']:
            response = self.validate(algorithm=algorithm)
            self.ok_test(response)

    def test_check_wrong_url(self):
        if self.REQUEST_URL is None:
            return
        response = self.validate(url='https://dfva.cr/ups')
        self.check_wrong_url_test(response)

    def test_check_wrong_institution(self):
        if self.REQUEST_URL is None:
            return
        response = self.validate(institution='no institution')
        self.check_wrong_institution_test(response)

    def test_check_wrong_sign(self):
        """if all credential are well but data is encrypted with other private
        key"""
        if self.REQUEST_URL is None:
            return
        institution2 = create_institution(self.user)
        url = "https://institution2.com/notify"
        create_url(institution2, url=url)

        response = self.validate(institution=str(institution2.code),
                                 url=url,
                                 public_certificate=institution2.public_certificate)

        response = decrypt(institution2.private_key,
                           response.data['data'])
        self.check_wrong_sign_test(response)

    def test_wrong_hashsum(self):
        if self.REQUEST_URL is None:
            return
        response = self.validate(
            hashsum="bd267a725dc16fc0fa33c267af52a25779b8dd628d0df26e5e8813505df8bef05")
        self.wrong_hashsum_test(response)

    def test_wrong_certificate(self):
        if self.REQUEST_URL is None:
            return
        response = self.validate(
            public_certificate=WRONG_CERTIFICATE
        )
        self.wrong_certificate_test(response)
