# encoding: utf-8

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

'''
@date: 16/8/2017
@author: Universidad de Costa Rica
@maintainer: Luis Zarate Montero
@contact: luis.zarate@solvosoft.com
@license: GPLv3
'''

from django.contrib.auth.models import User
from rest_framework.test import APIClient
import json
from corebase.rsa import encrypt, get_hash_sum
from corebase.test.institution_utils import create_institution, create_url
from django.test.testcases import TestCase
from django.conf import settings

class BaseInstitutionTest(TestCase):

    URL_NOTIFICATION = 'https://dfva.cr/notification'
    IDENTIFICATION = '08-0888-0888'
    ALGORITHM = 'sha512'
    REASON = None
    PLACE = None

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
        self.assertNotEqual(response['code'], 'N/D')
        self.assertEqual(response['status'], settings.DEFAULT_SUCCESS_BCCR)

    def check_wrong_url_test(self, response):
        self.assertEqual(response['code'], 'N/D')
        self.assertTrue('notification_url' in response['error_info'])
        self.assertEqual(response['status'], 2)
        self.assertEqual(response['id_transaction'], 0)

    def check_wrong_idtransaction_test(self, response):
        self.assertEqual(response['code'], 'N/D')
        self.assertEqual(response['status'], 2)
        self.assertEqual(response['id_transaction'], 0)

    def check_wrong_institution_test(self, response):
        self.assertEqual(response['code'], 'N/D')
        self.assertTrue('institution' in response['error_info'])
        self.assertEqual(response['status'], 2)
        self.assertEqual(response['id_transaction'], 0)

    def check_wrong_sign_test(self, response):
        self.assertEqual(response['code'], 'N/D')
        self.assertTrue('data' in response['error_info'])
        self.assertEqual(response['status'], 2)
        self.assertEqual(response['id_transaction'], 0)

    def wrong_hashsum_test(self, response):
        self.assertEqual(response['code'], 'N/D')
        self.assertTrue('data_hash' in response['error_info'])
        self.assertEqual(response['status'], 2)
        self.assertEqual(response['id_transaction'], 0)

    def wrong_certificate_test(self, response):
        self.assertEqual(response['code'], 'N/D')
        self.assertTrue('public_certificate' in response['error_info'])
        self.assertEqual(response['status'], 2)
        self.assertEqual(response['id_transaction'], 0)
