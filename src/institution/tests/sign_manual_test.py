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
import json
from corebase.rsa import encrypt, get_hash_sum
import requests
from corebase.test.environment import *
from corebase.test.documents import XMLFILE, HASHXML, ODFFILE, HASHODF, DOCXFILE,\
    HASHDOCX


def test_xml_signer(identificacion, url=LISTEN_URL):

    data = {
        'institution': INSTITUTION,
        'notification_url': url,
        'document': XMLFILE,
        'format': 'xml',
        'algorithm_hash': 'sha512',
        'document_hash': HASHXML,
        'identification': identificacion,
        'resumen': 'Documento de prueba xml',
        'request_datetime': timezone.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    algorithm = ALGORITHM
    str_data = json.dumps(data)
    # print(str_data)
    edata = encrypt(SERVER_PUBLIC_KEY, str_data)
    hashsum = get_hash_sum(edata,  ALGORITHM)
    edata = edata.decode()
    params = {
        "data_hash": hashsum,
        "algorithm": algorithm,
        "public_certificate": PUBLIC_CERTIFICATE,
        'institution': INSTITUTION,
        "data": edata,
    }
    result = requests.post(
        SERVER_URL + '/sign/institution/', json=params)

    data = result.json()
    # print(data)
    return data


def test_odf_signer(identificacion, url=LISTEN_URL):

    data = {
        'institution': INSTITUTION,
        'notification_url': url,
        'document': ODFFILE,
        'format': 'odf',
        'algorithm_hash': 'sha512',
        'document_hash': HASHODF,
        'identification': identificacion,
        'resumen': 'Documento de prueba odf',
        'request_datetime': timezone.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    algorithm = ALGORITHM
    str_data = json.dumps(data)
    # print(str_data)
    edata = encrypt(SERVER_PUBLIC_KEY, str_data)
    hashsum = get_hash_sum(edata,  ALGORITHM)
    edata = edata.decode()
    params = {
        "data_hash": hashsum,
        "algorithm": algorithm,
        "public_certificate": PUBLIC_CERTIFICATE,
        'institution': INSTITUTION,
        "data": edata,
    }
    result = requests.post(
        SERVER_URL + '/sign/institution/', json=params)

    data = result.json()
    print(data)
    return data


def test_msoffice_signer(identificacion, url=LISTEN_URL):

    data = {
        'institution': INSTITUTION,
        'notification_url': url,
        'document': DOCXFILE,
        'format': 'msoffice',
        'algorithm_hash': 'sha512',
        'document_hash': HASHDOCX,
        'identification': identificacion,
        'resumen': 'Documento de prueba odf',
        'request_datetime': timezone.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    algorithm = ALGORITHM
    str_data = json.dumps(data)
    # print(str_data)
    edata = encrypt(SERVER_PUBLIC_KEY, str_data)
    hashsum = get_hash_sum(edata,  ALGORITHM)
    edata = edata.decode()
    params = {
        "data_hash": hashsum,
        "algorithm": algorithm,
        "public_certificate": PUBLIC_CERTIFICATE,
        'institution': INSTITUTION,
        "data": edata,
    }
    result = requests.post(
        SERVER_URL + '/sign/institution/', json=params)

    data = result.json()
    print(data)
    return data


def test_signer_show(identificacion, url=LISTEN_URL):
    signdata = test_xml_signer(identificacion, url=LISTEN_URL)
    print(signdata)
    data = {
        'institution': INSTITUTION,
        'notification_url': url,
        'identification': identificacion,
        'request_datetime': timezone.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    algorithm = ALGORITHM
    str_data = json.dumps(data)
    # print(str_data)
    edata = encrypt(SERVER_PUBLIC_KEY, str_data)
    hashsum = get_hash_sum(edata,  ALGORITHM)
    edata = edata.decode()
    params = {
        "data_hash": hashsum,
        "algorithm": algorithm,
        "public_certificate": PUBLIC_CERTIFICATE,
        'institution': INSTITUTION,
        "data": edata,
    }
    result = requests.post(
        SERVER_URL + '/sign/%s/institution_show/' % (signdata['code'], ), json=params)

    data = result.json()
    return data
