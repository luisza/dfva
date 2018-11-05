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
from corebase.test import CERTIFICATE_FILE


def test_validate_certificate(url=LISTEN_URL):

    data = {
        'institution': INSTITUTION,
        'notification_url': url,
        'document': CERTIFICATE_FILE,
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
        SERVER_URL + '/validate/institution_certificate/', json=params)

    # print(params)
    data = result.json()
    print(data)


def test_validate_document(url=LISTEN_URL):

    data = {
        'institution': INSTITUTION,
        'notification_url': url,
        'document': CERTIFICATE_FILE,
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
        SERVER_URL + '/validate/institution_document/', json=params)

    # print(params)
    data = result.json()
    print(data)
