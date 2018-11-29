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
@author: Universidad de Costa Rica
@maintainer: Luis Zarate Montero
@contact: luis.zarate@solvosoft.com
@license: GPLv3
'''

from django.utils import timezone
import json
from corebase.rsa import encrypt, get_hash_sum
import requests
from corebase.test.environment import *


def test_authentication(identificacion, url=LISTEN_URL):

    data = {
        'institution': INSTITUTION,
        'notification_url': url,
        'identification': identificacion,
        'request_datetime': timezone.now().isoformat(),
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
        SERVER_URL + '/authenticate/institution/', json=params)

    # print(params)
    data = result.json()
    return data


def test_authentication_detail(identificacion, url=LISTEN_URL):
    authdata = test_authentication(identificacion, url=LISTEN_URL)
    data = {
        'institution': INSTITUTION,
        'notification_url': url,
        'identification': identificacion,
        'request_datetime': timezone.now().isoformat(),
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
        SERVER_URL + "/authenticate/%s/institution_show/" % (authdata['code']), json=params)

    # print(params)
    data = result.json()
    return data
