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
@date: 19/8/2017
@author: Luis Zarate Montero
@contact: luis.zarate@solvosoft.com
@license: GPLv3
'''

from corebase.test.person import BasePersonTest
from corebase.test.documents import XMLFILE, ODFFILE, DOCXFILE
from person.models import SignPersonDataRequest
from corebase.test.institution_utils import create_institution


class SignPersonCase(BasePersonTest):

    def sign(self, **kwargs):
        identification = kwargs.get('identification', self.person)
        document = kwargs.get('document', None)
        algorithm = kwargs.get('algorithm', 'sha512')
        file_path = kwargs.get('file_path', None)
        is_base64 = kwargs.get('is_base64', False)
        _format = kwargs.get('_format', 'xml_cofirma')
        resume = kwargs.get('resume', 'Resumen de documento')
        response = self.client.sign(
            identification,
            document,
            resume,
            algorithm=algorithm,
            file_path=file_path, _format=_format, is_base64=is_base64)

        return response

    def test_sign_xml_cofirma(self):
        self._test_sign_xml(_format='xml_cofirma')

    def _test_sign_xml(self, algorithm='sha512', _format='xml_cofirma'):
        response = self.sign(document=XMLFILE,
                             algorithm=algorithm,
                             _format=_format,
                             is_base64=True)
        self.ok_test(response)
        self.assertIsNotNone(SignPersonDataRequest.objects.filter(
            code=response['code']).first())

    def test_sign_xml_contrafirma(self):
        self._test_sign_xml(_format='xml_contrafirma')

    def test_sign_odf(self):
        self._test_sign_odf()

    def _test_sign_odf(self, algorithm='sha512'):
        response = self.sign(document=ODFFILE,
                             _format="odf",
                             algorithm=algorithm,
                             is_base64=True)
        self.ok_test(response)
        self.assertIsNotNone(SignPersonDataRequest.objects.filter(
            code=response['code']).first())

    def test_sign_msoffice(self):
        self._test_sign_msoffice()

    def _test_sign_msoffice(self, algorithm='sha512'):
        response = self.sign(document=DOCXFILE,
                             _format="msoffice",
                             is_base64=True)
        self.ok_test(response)
        self.assertIsNotNone(SignPersonDataRequest.objects.filter(
            code=response['code']).first())

    def test_algorithms_xml_cofirma(self):
        for algorithm in ['sha256', 'sha384', 'sha512']:
            self._test_sign_xml(algorithm=algorithm, _format='xml_cofirma')

    def test_algorithms_xml_contrafirma(self):
        for algorithm in ['sha256', 'sha384', 'sha512']:
            self._test_sign_xml(algorithm=algorithm, _format='xml_contrafirma')

    def test_algorithms_odf(self):
        for algorithm in ['sha256', 'sha384', 'sha512']:
            self._test_sign_odf(algorithm=algorithm)

    def test_algorithms_msoffice(self):
        for algorithm in ['sha256', 'sha384', 'sha512']:
            self._test_sign_msoffice(algorithm=algorithm)

    def test_own_sign(self):
        response = self.own_sign(
            document=XMLFILE,
            is_base64=True
        )
        self.ok_test(response)
        self.assertIsNotNone(SignPersonDataRequest.objects.filter(
            code=response['code']).first())

    def test_wrong_format(self):
        response = self.own_sign(document=XMLFILE,
                                 is_base64=True,
                                 _format='pdf')
        self.wrong_format(response)

    def test_check_wrong_sign(self):
        """if all credential are well but data is encrypted with other private
        key"""
        institution2 = create_institution(self.user)
#         url = "https://institution2.com/notify"
#         create_url(institution2, url=url)

        def edata_fun(str_data, etype='sign'):
            return self.dummy_encrypt(str_data, institution2.public_key)

        response = self.own_sign(
            document=XMLFILE,
            is_base64=True,
            edata=edata_fun,
            public_certificate=institution2.public_certificate)
        self.check_wrong_sign_test(response)
#

    def test_wrong_hashsum(self):
        response = self.own_sign(
            document=XMLFILE,
            is_base64=True,
            hashsum="bd267a725dc16fc0fa33c267af52a25779b8dd628d0df26e5e8813505df8bef05")
        self.wrong_hashsum_test(response)

#     def test_wrong_certificate(self):
#
#         response = self.own_sign(
#             document=XMLFILE,
#             is_base64=True,
#             public_certificate=WRONG_CERTIFICATE
#         )
#         self.wrong_certificate_test(response)
