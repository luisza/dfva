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

from corebase.rsa import decrypt
import json
from institution.models import AuthenticateDataRequest
from corebase.test.institution_utils import create_institution, create_url
from django.utils import timezone


from corebase.test.institution import BaseInstitutionTest
from corebase.test import WRONG_CERTIFICATE


class CheckAuthenticatorInstitutionCase(BaseInstitutionTest):
    BASE_URL = '/authenticate/%s/institution_show/'

    def setUp(self):
        super(CheckAuthenticatorInstitutionCase, self).setUp()
        response = self.authenticate(identification=self.IDENTIFICATION)
        self.data = response
        # print(self.data)

    def authenticate(self, **kwargs):

        url = kwargs.get('url', self.URL_NOTIFICATION)
        institution = kwargs.get('institution', str(self.institution.code))
        request_datetime = kwargs.get(
            'request_datetime', timezone.now().isoformat())
        identification = kwargs.get('identification', None)
        request_url = kwargs.get('request_url', '/authenticate/institution/')
        data = {
            'institution': institution,
            'notification_url': url,
            'request_datetime': request_datetime,
        }

        if identification:
            data['identification'] = identification

        params = self.get_request_params(data, **kwargs)

        response = self.client.post(request_url,
                                    params, format='json')
        try:
            response = decrypt(self.institution.private_key,
                               response.data['data'])
        except Exception as e:
            try:
                response = json.loads(response.json()['data'])
            except:
                pass

        return response

    def test_authenticate_check(self):
        response = self.authenticate(identification=self.IDENTIFICATION)
        self.ok_test(response)
        self.assertIsNotNone(AuthenticateDataRequest.objects.filter(
            code=response['code']).first())
        response = self.authenticate(
            request_url=self.BASE_URL % (response['id_transaction'],))

        self.ok_test(response)

    def test_algorithms(self):

        for algorithm in ['sha256', 'sha384', 'sha512']:
            response = self.authenticate(algorithm=algorithm,
                                         identification=self.IDENTIFICATION)
            response = self.authenticate(
                algorithm=algorithm,
                request_url=self.BASE_URL % (response['id_transaction'],))
            self.ok_test(response)

    def test_check_wrong_url(self):
        response = self.authenticate(
            url='https://dfva.cr/ups',
            request_url=self.BASE_URL % (self.data['id_transaction'],))
        self.check_wrong_url_test(response)

    def test_check_wrong_institution(self):
        response = self.authenticate(
            institution='no institution',
            request_url=self.BASE_URL % (self.data['id_transaction'],)
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
                                         self.data['id_transaction'],)
                                     )
        response = decrypt(institution2.private_key,
                           response.data['data'])
        self.check_wrong_sign_test(response)

    def test_wrong_hashsum(self):
        response = self.authenticate(request_url=self.BASE_URL % (
            self.data['id_transaction'],),
            hashsum="bd267a725dc16fc0fa33c267af52a25779b8dd628d0df26e5e8813505df8bef05")
        self.wrong_hashsum_test(response)

    def test_wrong_certificate(self):

        response = self.authenticate(request_url=self.BASE_URL % (
            self.data['id_transaction'],),
            public_certificate=WRONG_CERTIFICATE
        )
        self.wrong_certificate_test(response)

    def test_wrong_id_trasaction(self):
        response = self.authenticate(
            request_url=self.BASE_URL % ("02345232",))
        self.check_wrong_idtransaction_test(response)
