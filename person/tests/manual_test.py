'''
Created on 16 ago. 2017

@author: luis
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
