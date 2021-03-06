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
@date: 15/8/2017
@author: Luis Zarate Montero
@contact: luis.zarate@solvosoft.com
@license: GPLv3
'''

from corebase.test.person import BasePersonTest
from corebase.test.institution_utils import create_institution
from person.models import AuthenticatePersonDataRequest


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
