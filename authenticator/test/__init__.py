

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
        SERVER_URL + '/authenticate/', json=params)

    # print(params)
    data = result.json()
    return data


def test_authentication_detail(identificacion, url=LISTEN_URL):
    authdata = test_authentication(identificacion, url=LISTEN_URL)
    print(authdata)
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
        SERVER_URL + "/authenticate/%s/show/" % (authdata['code']), json=params)

    # print(params)
    data = result.json()
    return data
