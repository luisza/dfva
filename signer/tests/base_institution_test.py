'''
Created on 16 ago. 2017

@author: luis
'''
from corebase.test.institution import BaseInstitutionTest
from corebase.test.institutio_utils import create_institution, create_url
from signer.models import SignDataRequest
from django.utils import timezone
from authenticator.tests import WRONG_CERTIFICATE
import json
from corebase.rsa import decrypt


class SignCase(BaseInstitutionTest):
    DOCUMENT = None
    HASH = None
    FORMAT = 'xml'

    def sign(self, **kwargs):
        url = kwargs.get('url', self.URL_NOTIFICATION)
        institution = kwargs.get('institution', str(self.institution.code))
        request_datetime = kwargs.get(
            'request_datetime', timezone.now().isoformat())
        resumen = kwargs.get('resumen', 'Documento de prueba xml')
        identificacion = kwargs.get('identificacion', self.IDENTIFICATION)
        data = {
            'institution': institution,
            'notification_url': url,
            'document': self.DOCUMENT,
            'format': self.FORMAT,
            'algorithm_hash': 'sha512',
            'document_hash': self.HASH,
            'identification': identificacion,
            'resumen': resumen,
            'request_datetime': request_datetime,
        }
        params = self.get_request_params(data, **kwargs)

        response = self.client.post('/sign/institution/',
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
        if self.DOCUMENT is None:
            return
        response = self.sign()
        self.ok_test(response)
        self.assertIsNotNone(SignDataRequest.objects.filter(
            code=response['code']).first())

    def test_algorithms(self):
        if self.DOCUMENT is None:
            return
        for algorithm in ['sha256', 'sha384', 'sha512']:
            response = self.sign(algorithm=algorithm)
            self.ok_test(response)

    def test_check_wrong_url(self):
        if self.DOCUMENT is None:
            return
        response = self.sign(url='https://dfva.cr/ups')
        self.check_wrong_url_test(response)

    def test_check_wrong_institution(self):
        if self.DOCUMENT is None:
            return
        response = self.sign(institution='no institution')
        self.check_wrong_institution_test(response)

    def test_check_wrong_sign(self):
        """if all credential are well but data is encrypted with other private
        key"""
        if self.DOCUMENT is None:
            return
        institution2 = create_institution(self.user)
        url = "https://institution2.com/notify"
        create_url(institution2, url=url)

        response = self.sign(institution=str(institution2.code),
                             url=url,
                             public_certificate=institution2.public_certificate)
        response = decrypt(institution2.private_key,
                           response.data['data'])
        self.check_wrong_sign_test(response)

    def test_wrong_hashsum(self):
        if self.DOCUMENT is None:
            return
        response = self.sign(
            hashsum="bd267a725dc16fc0fa33c267af52a25779b8dd628d0df26e5e8813505df8bef05")
        self.wrong_hashsum_test(response)

    def test_wrong_certificate(self):
        if self.DOCUMENT is None:
            return
        response = self.sign(
            public_certificate=WRONG_CERTIFICATE
        )
        self.wrong_certificate_test(response)


class CheckSignCase(BaseInstitutionTest):
    DOCUMENT = None
    HASH = None
    FORMAT = 'xml'
    BASE_URL = '/sign/%s/institution_show/'

    def setUp(self):
        if self.DOCUMENT is None:
            return
        super(CheckSignCase, self).setUp()
        response = self.sign()
        self.data = response

    def sign(self, **kwargs):
        if self.DOCUMENT is None:
            return
        url = kwargs.get('url', self.URL_NOTIFICATION)
        institution = kwargs.get('institution', str(self.institution.code))
        request_datetime = kwargs.get(
            'request_datetime', timezone.now().isoformat())
        resumen = kwargs.get('resumen', 'Documento de prueba xml')
        identificacion = kwargs.get('identificacion', self.IDENTIFICATION)
        data = {
            'institution': institution,
            'notification_url': url,
            'document': self.DOCUMENT,
            'format': self.FORMAT,
            'algorithm_hash': 'sha512',
            'document_hash': self.HASH,
            'identification': identificacion,
            'resumen': resumen,
            'request_datetime': request_datetime,
        }
        params = self.get_request_params(data, **kwargs)

        response = self.client.post('/sign/institution/',
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

    def test_authenticate_check(self):
        if self.DOCUMENT is None:
            return
        response = self.sign()
        self.ok_test(response)
        self.assertIsNotNone(SignDataRequest.objects.filter(
            code=response['code']).first())

        response = self.sign(
            request_url=self.BASE_URL % (response['code'],))
        self.ok_test(response)

    def test_algorithms(self):
        if self.DOCUMENT is None:
            return
        for algorithm in ['sha256', 'sha384', 'sha512']:
            response = self.sign(algorithm=algorithm)
            response = self.sign(
                algorithm=algorithm,
                request_url=self.BASE_URL % (response['code'],))
            self.ok_test(response)

    def test_check_wrong_url(self):
        if self.DOCUMENT is None:
            return
        response = self.sign(
            url='https://dfva.cr/ups',
            request_url=self.BASE_URL % (self.data['code'],))
        self.check_wrong_url_test(response)

    def test_check_wrong_institution(self):
        if self.DOCUMENT is None:
            return
        response = self.sign(
            institution='no institution',
            request_url=self.BASE_URL % (self.data['code'],)
        )
        self.check_wrong_institution_test(response)

    def test_check_wrong_sign(self):
        """if all credential are well but data is encrypted with other private
        key"""
        if self.DOCUMENT is None:
            return
        institution2 = create_institution(self.user)
        url = "https://institution2.com/notify"
        create_url(institution2, url=url)

        response = self.sign(institution=str(institution2.code),
                             url=url,
                             public_certificate=institution2.public_certificate,
                             request_url=self.BASE_URL % (
            self.data['code'],)
        )
        response = decrypt(institution2.private_key,
                           response.data['data'])
        self.check_wrong_sign_test(response)

    def test_wrong_hashsum(self):
        if self.DOCUMENT is None:
            return
        response = self.sign(request_url=self.BASE_URL % (
            self.data['code'],),
            hashsum="bd267a725dc16fc0fa33c267af52a25779b8dd628d0df26e5e8813505df8bef05")
        self.wrong_hashsum_test(response)

    def test_wrong_certificate(self):
        if self.DOCUMENT is None:
            return
        response = self.sign(request_url=self.BASE_URL % (
            self.data['code'],),
            public_certificate=WRONG_CERTIFICATE
        )
        self.wrong_certificate_test(response)
