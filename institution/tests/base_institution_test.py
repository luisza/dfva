'''
Created on 16 ago. 2017

@author: luis
'''
from corebase.test.institution import BaseInstitutionTest
from django.utils import timezone

import json
from corebase.rsa import decrypt
from corebase.test.institution_utils import create_institution, create_url
from institution.models import SignDataRequest
from corebase.test import WRONG_CERTIFICATE


class SignCase(BaseInstitutionTest):
    DOCUMENT = None
    HASH = None
    FORMAT = None

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

    def sign_check(self, **kwargs):
        if self.DOCUMENT is None:
            return
        url = kwargs.get('url', self.URL_NOTIFICATION)
        institution = kwargs.get('institution', str(self.institution.code))
        request_datetime = kwargs.get(
            'request_datetime', timezone.now().isoformat())
        request_url=kwargs.get('request_url', '/sign/institution/')
        
        data = {
            'institution': institution,
            'notification_url': url,
            'request_datetime': request_datetime,
        }
      
        params = self.get_request_params(data, **kwargs)
        response = self.client.post(request_url,
                                    params, format='json')
        try:
            response = decrypt(self.institution.private_key,
                               response.data['data'])
        except Exception as e:
            #print(e)
            try:
                response = json.loads(response.json()['data'])
            except:
                pass
        return response
                
    def sign(self, **kwargs):
        if self.DOCUMENT is None:
            return
        url = kwargs.get('url', self.URL_NOTIFICATION)
        institution = kwargs.get('institution', str(self.institution.code))
        request_datetime = kwargs.get(
            'request_datetime', timezone.now().isoformat())
        resumen = kwargs.get('resumen', 'Documento de prueba xml')
        identificacion = kwargs.get('identificacion', self.IDENTIFICATION)
        request_url=kwargs.get('request_url', '/sign/institution/')
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

    def test_authenticate_check(self):
        if self.DOCUMENT is None:
            return
        response = self.sign()
        self.ok_test(response)
        self.assertIsNotNone(SignDataRequest.objects.filter(
            code=response['code']).first())

        response = self.sign_check(
            request_url=self.BASE_URL % (response['id_transaction'],))
        self.ok_test(response)

    def test_algorithms(self):
        if self.DOCUMENT is None:
            return
        for algorithm in ['sha256', 'sha384', 'sha512']:
            response = self.sign(algorithm=algorithm)
            response = self.sign_check(
                algorithm=algorithm,
                request_url=self.BASE_URL % (response['id_transaction'],))
            self.ok_test(response)

    def test_wrong_id_transaction(self):
        if self.DOCUMENT is None:
            return
        response = self.sign_check(
            request_url=self.BASE_URL % ("123456789",))
        self.check_wrong_idtransaction_test(response)

    def test_check_wrong_url(self):
        if self.DOCUMENT is None:
            return
        response = self.sign_check(
            url='https://dfva.cr/ups',
            request_url=self.BASE_URL % (self.data['id_transaction'],))
        self.check_wrong_url_test(response)

    def test_check_wrong_institution(self):
        if self.DOCUMENT is None:
            return
        response = self.sign_check(
            institution='no institution',
            request_url=self.BASE_URL % (self.data['id_transaction'],)
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

        response = self.sign_check(institution=str(institution2.code),
                             url=url,
                             public_certificate=institution2.public_certificate,
                             request_url=self.BASE_URL % (
            self.data['id_transaction'],)
        )
        response = decrypt(institution2.private_key,
                           response.data['data'])
        self.check_wrong_sign_test(response)

    def test_wrong_hashsum(self):
        if self.DOCUMENT is None:
            return
        response = self.sign_check(request_url=self.BASE_URL % (
            self.data['id_transaction'],),
            hashsum="bd267a725dc16fc0fa33c267af52a25779b8dd628d0df26e5e8813505df8bef05")
        self.wrong_hashsum_test(response)

    def test_wrong_certificate(self):
        if self.DOCUMENT is None:
            return
        response = self.sign_check(request_url=self.BASE_URL % (
            self.data['id_transaction'],),
            public_certificate=WRONG_CERTIFICATE
        )
        self.wrong_certificate_test(response)


class DeleteSignCase(BaseInstitutionTest):
    DOCUMENT = None
    HASH = None
    FORMAT = 'xml'
    BASE_URL = '/sign/%s/institution_delete/'

    def setUp(self):
        if self.DOCUMENT is None:
            return
        super(DeleteSignCase, self).setUp()
        response = self.sign()
        self.data = response

    def sign_delete(self, **kwargs):
        if self.DOCUMENT is None:
            return
        url = kwargs.get('url', self.URL_NOTIFICATION)
        institution = kwargs.get('institution', str(self.institution.code))
        request_datetime = kwargs.get(
            'request_datetime', timezone.now().isoformat())
        request_url=kwargs.get('request_url', '/sign/institution/')
        
        data = {
            'institution': institution,
            'notification_url': url,
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

    def check_result(self, response, status=True):
        self.assertEqual(response['result'], status)

    def test_authenticate_check(self):
        if self.DOCUMENT is None:
            return
        response = self.sign()
        self.ok_test(response)
        self.assertIsNotNone(SignDataRequest.objects.filter(
            code=response['code']).first())
        id_transaction=response['id_transaction']
        response = self.sign_delete(
            request_url=self.BASE_URL % (response['id_transaction'],))
        
        
        self.check_result(response)
        self.assertIsNone(SignDataRequest.objects.filter(
            id_transaction=id_transaction).first())
        
    def test_wrong_id_trasaction(self):
        if self.DOCUMENT is None:
            return
        response = self.sign_delete(
            request_url=self.BASE_URL % ("0123232344583",))
        self.check_result(response, False)

        
    def test_algorithms(self):
        if self.DOCUMENT is None:
            return
        for algorithm in ['sha256', 'sha384', 'sha512']:
            response = self.sign(algorithm=algorithm)
            response = self.sign_delete(
                algorithm=algorithm,
                request_url=self.BASE_URL % (response['id_transaction'],))
            self.check_result(response)

    def test_check_wrong_url(self):
        if self.DOCUMENT is None:
            return
        response = self.sign_delete(
            url='https://dfva.cr/ups',
            request_url=self.BASE_URL % (self.data['id_transaction'],))
        self.check_result(response, False)
        self.assertIsNotNone(SignDataRequest.objects.filter(
            id_transaction=self.data['id_transaction']).first())

    def test_check_wrong_institution(self):
        if self.DOCUMENT is None:
            return

        response = self.sign_delete(
            institution='no institution',
            request_url=self.BASE_URL % (self.data['id_transaction'],)
        )
        self.check_result(response, False)
        self.assertIsNotNone(SignDataRequest.objects.filter(
            id_transaction=self.data['id_transaction']).first())


    def test_check_wrong_sign(self):
        """if all credential are well but data is encrypted with other private
        key"""
        if self.DOCUMENT is None:
            return
        institution2 = create_institution(self.user)
        url = "https://institution2.com/notify"
        create_url(institution2, url=url)
        
        response = self.sign_delete(institution=str(institution2.code),
                             url=url,
                             public_certificate=institution2.public_certificate,
                             request_url=self.BASE_URL % (
            self.data['id_transaction'],)
        )
        response = decrypt(institution2.private_key,
                           response.data['data'])
        self.check_result(response,  False)
        self.assertIsNotNone(SignDataRequest.objects.filter(
            id_transaction=self.data['id_transaction']).first())


    def test_wrong_hashsum(self):
        if self.DOCUMENT is None:
            return
        response = self.sign_delete(request_url=self.BASE_URL % (
            self.data['id_transaction'],),
            hashsum="bd267a725dc16fc0fa33c267af52a25779b8dd628d0df26e5e8813505df8bef05")
        self.check_result(response, False)
        self.assertIsNotNone(SignDataRequest.objects.filter(
            id_transaction=self.data['id_transaction']).first())


    def test_wrong_certificate(self):
        if self.DOCUMENT is None:
            return
        response = self.sign_delete(request_url=self.BASE_URL % (
            self.data['id_transaction'],),
            public_certificate=WRONG_CERTIFICATE
        )
        self.check_result(response, False)
        self.assertIsNotNone(SignDataRequest.objects.filter(
            id_transaction=self.data['id_transaction']).first())



class BaseValidateInstitutionCase(BaseInstitutionTest):
    REQUEST_URL = None
    DATAREQUEST = None
    FORMAT=None

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
        if self.FORMAT:
            data['format']=self.FORMAT
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