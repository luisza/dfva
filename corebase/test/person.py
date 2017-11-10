'''
Created on 18 ago. 2017

@author: luis
'''
from django.contrib.auth.models import User
from asyncio.test_utils import TestCase
from corebase.test.institution_utils import create_institution, create_url
from rest_framework.test import APIClient
import json
from corebase.rsa import get_hash_sum, encrypt, decrypt as decrypt_base
from client_fva.person import PersonClient
from client_fva.rsa import decrypt
from client_fva.user_settings import UserSettings as Settings
from base64 import b64encode
from django.utils import timezone
from person.models import Person


class HTTPClient():

    def __init__(self, apiclient):
        self.apiclient = apiclient

    def post(self, url, json={}, headers={}, format='json'):
        return self.apiclient.post(url, json,  format=format)

    def get(self, url, json={}, headers={}, format='json'):
        return self.apiclient.get(url, json,  format=format)


class BasePersonTest(TestCase):
    person = '04-0212-0119'
    IDENTIFICATION = '08-0888-0888'
    ALGORITHM = 'sha512'
    URL_NOTIFICATION = 'https://dfva.cr/notification'

    def setUp(self):
        try:
            self.user = User.objects.create_user(
                username='test', email='test@dfva.cr', password='top_secret')
        except:
            self.user = User.objects.first()
        self.institution = create_institution(self.user)
        create_url(self.institution, url=self.URL_NOTIFICATION)
        create_url(self.institution)
        self.request_client = HTTPClient(APIClient())
        self.settings = Settings()
        self.settings.fva_server_url = ''

        self.client = PersonClient(settings=self.settings,
                                   request_client=self.request_client)

        self.person = self.client.get_identification()
        auth_cert = self.client.get_certificates()['authentication']
        self.person_obj, _ = Person.objects.get_or_create(
            user=self.user,
            identification=self.person)
        self.person_obj.authenticate_certificate = auth_cert
        self.client.register()

    def _decrypt(self, str_data):
        etype = 'authentication'
        keys = self.client.get_keys()
        return decrypt(keys[etype]['priv_key'], str_data)

    def tearDown(self):
        self.client.unregister()
        #super(BasePersonTest, self).tearDown()

    def get_request_params(self, data, **kwargs):

        algorithm = kwargs.get('algorithm', self.ALGORITHM)
        str_data = json.dumps(data)

        use = kwargs.get('use', 'sign')
        edata_fun = kwargs.get('edata', None)
        if edata_fun:
            edata = edata_fun(str_data, etype=use)
        else:
            edata = self.client._encrypt(str_data, etype=use)
        hashsum = kwargs.get('hashsum', get_hash_sum(edata,  algorithm))
        edata = edata.decode()

        if use == 'sign':
            tmpcert = self.client._get_public_sign_certificate()
        else:
            tmpcert = self.client._get_public_auth_certificate()
        certificate = kwargs.get('public_certificate', tmpcert)

        person = kwargs.get('person', self.person)
        params = {
            "data_hash": hashsum,
            "algorithm": algorithm,
            "public_certificate": certificate,
            'person': person,
            "data": edata,
        }
        return params

    def dummy_encrypt(self, data, public_key):
        return encrypt(public_key, data)

    def dummy_decrypt(self, private_key, data):
        return decrypt_base(private_key, data)

    def own_authenticate(self, **kwargs):
        identification = kwargs.get('identification', self.person)
        person = kwargs.get('person', self.person)
        request_datetime = kwargs.get(
            'request_datetime', timezone.now().isoformat())
        data = {
            'person': person,
            'identification': identification,
            'request_datetime': request_datetime
        }
        params = self.get_request_params(data, **kwargs)
        result = self.request_client.post(
            self.settings.fva_server_url +
            self.settings.authenticate_person, json=params)

        data = result.json()
        data = self._decrypt(data['data'])
        try:
            data = self._decrypt(data['data'])
        except Exception as e:
            pass
        return data

    def own_sign(self, **kwargs):

        identification = kwargs.get('identification', self.person)
        person = kwargs.get('person', self.person)
        document = kwargs.get('document', None)
        algorithm = kwargs.get('algorithm', 'sha512')
        is_base64 = kwargs.get('is_base64', False)
        _format = kwargs.get('_format', 'xml')
        resume = kwargs.get('resume', 'resumen magnifico')
        request_datetime = kwargs.get(
            'request_datetime', timezone.now().isoformat())

        if not is_base64:
            document = b64encode(document).decode()

        data = {
            'person': person,
            'document': document,
            'format': _format,
            'algorithm_hash': algorithm,
            'document_hash': get_hash_sum(document,  algorithm),
            'identification': identification,
            'resumen': resume,
            'request_datetime': request_datetime,
        }
        params = self.get_request_params(data, **kwargs)
        headers = {'Accept': 'application/json',
                   'Content-Type': 'application/json'}

        result = self.request_client.post(
            self.settings.fva_server_url + self.settings.sign_person,
            json=params, headers=headers)

        data = result.json()
        try:
            data = self._decrypt(data['data'])
        except:
            pass
        return data

    def ok_test(self, response):
        self.assertNotEqual(response['code'], 'N/D')
        self.assertEqual(response['status'], 1)

    def wrong_format(self, response):
        self.assertEqual(response['code'], 'N/D')
        self.assertEqual(response['status'], 2)
        self.assertTrue('format' in response['error_info'])

    def wrong_hashsum_test(self, response):
        self.assertEqual(response['code'], 'N/D')
        self.assertTrue('data_hash' in response['error_info'])
        self.assertEqual(response['status'], 2)
        self.assertEqual(response['id_transaction'], 0)

    def check_wrong_sign_test(self, response):
        self.assertEqual(response['code'], 'N/D')
        self.assertTrue('data' in response['error_info'])
        self.assertEqual(response['status'], 2)
        self.assertEqual(response['id_transaction'], 0)

    def wrong_certificate_test(self, response):
        self.assertEqual(response['code'], 'N/D')
        self.assertTrue('public_certificate' in response['error_info'])
        self.assertEqual(response['status'], 2)
        self.assertEqual(response['id_transaction'], 0)
