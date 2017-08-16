'''
Created on 16 ago. 2017

@author: luis
'''
from django.contrib.auth.models import User
from rest_framework.test import APIClient
import json
from corebase.rsa import encrypt, get_hash_sum
from corebase.test.institutio_utils import create_institution, create_url
from django.test.testcases import TestCase


class BaseInstitutionTest(TestCase):

    URL_NOTIFICATION = 'https://dfva.cr/notification'
    IDENTIFICATION = '08-0888-0888'
    ALGORITHM = 'sha512'

    def setUp(self):
        self.user = User.objects.create_user(
            username='test', email='test@dfva.cr', password='top_secret')
        self.institution = create_institution(self.user)
        create_url(self.institution, url=self.URL_NOTIFICATION)
        create_url(self.institution)

        self.client = APIClient()

    def get_request_params(self, data, **kwargs):

        algorithm = kwargs.get('algorithm', self.ALGORITHM)
        server_public_key = kwargs.get('server_public_key',
                                       self.institution.server_public_key)
        str_data = json.dumps(data)
        edata = encrypt(server_public_key, str_data)
        hashsum = kwargs.get('hashsum', get_hash_sum(edata,  algorithm))
        institution = kwargs.get('institution', str(self.institution.code))
        edata = edata.decode()
        certificate = kwargs.get('public_certificate',
                                 self.institution.public_certificate)
        params = {
            "data_hash": hashsum,
            "algorithm": algorithm,
            "public_certificate": certificate,
            'institution': institution,
            "data": edata,
        }
        return params

    def ok_test(self, response):
        self.assertNotEqual(response.data['code'], 'N/D')
        self.assertEqual(response.data['status'], 1)

    def check_wrong_url_test(self, response):
        self.assertEqual(response.data['code'], 'N/D')
        self.assertTrue('notification_url' in response.data['error_info'])
        self.assertEqual(response.data['status'], 2)
        self.assertEqual(response.data['id_transaction'], 0)

    def check_wrong_institution_test(self, response):
        self.assertEqual(response.data['code'], 'N/D')
        self.assertTrue('institution' in response.data['error_info'])
        self.assertEqual(response.data['status'], 2)
        self.assertEqual(response.data['id_transaction'], 0)

    def check_wrong_sign_test(self, response):
        self.assertEqual(response.data['code'], 'N/D')
        self.assertTrue('data' in response.data['error_info'])
        self.assertEqual(response.data['status'], 2)
        self.assertEqual(response.data['id_transaction'], 0)

    def wrong_hashsum_test(self, response):
        self.assertEqual(response.data['code'], 'N/D')
        self.assertTrue('data_hash' in response.data['error_info'])
        self.assertEqual(response.data['status'], 2)
        self.assertEqual(response.data['id_transaction'], 0)

    def wrong_certificate_test(self, response):
        self.assertEqual(response.data['code'], 'N/D')
        self.assertTrue('public_certificate' in response.data['error_info'])
        self.assertEqual(response.data['status'], 2)
        self.assertEqual(response.data['id_transaction'], 0)
