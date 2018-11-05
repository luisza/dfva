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
@author: Luis Zarate Montero
@contact: luis.zarate@solvosoft.com
@license: GPLv3
'''

from django.utils import timezone
from corebase.test.institution_utils import create_institution
from corebase.test.person import BasePersonTest


class BaseValidatePersonCase(BasePersonTest):
    REQUEST_URL = None
    DATAREQUEST = None
    DOCUMENT = None
    FORMAT = None

    def validate(self, **kwargs):
        person = kwargs.get('person', self.person)
        request_datetime = kwargs.get(
            'request_datetime', timezone.now().isoformat())
        certificate = kwargs.get('certificate', self.DOCUMENT)
        request_url = kwargs.get(
            'request_url', self.REQUEST_URL)
        data = {
            'person': person,
            'document': certificate,
            'request_datetime': request_datetime,
        }
        if self.FORMAT:
            data['format'] = self.FORMAT

        params = self.get_request_params(data, **kwargs)

        response = self.request_client.post(request_url,
                                            params, format='json')

        response = response.json()
        response = self._decrypt(response['data'])
        return response

    def test_validate(self):
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

    def test_check_wrong_encrypt_validation(self):
        """if all credential are well but data is encrypted with other private
        key"""
        if self.REQUEST_URL is None:
            return

        institution2 = create_institution(self.user)
#         url = "https://institution2.com/notify"
#         create_url(institution2, url=url)

        def edata_fun(str_data, etype='sign'):
            return self.dummy_encrypt(str_data, institution2.public_key)

        response = self.validate(
            edata=edata_fun,
            public_certificate=institution2.public_certificate
        )
        self.check_wrong_sign_test(response)

    def test_wrong_hashsum(self):
        if self.REQUEST_URL is None:
            return
        response = self.validate(
            hashsum="bd267a725dc16fc0fa33c267af52a25779b8dd628d0df26e5e8813505df8bef05")
        self.wrong_hashsum_test(response)

#     def test_wrong_certificate(self):
#         if self.REQUEST_URL is None:
#             return
#         response = self.validate(
#             public_certificate=WRONG_CERTIFICATE
#         )
#         print(response)
#         self.wrong_certificate_test(response)
