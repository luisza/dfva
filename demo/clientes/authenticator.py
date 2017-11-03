'''
Created on 26 jul. 2017

@author: luis
'''
from django.utils import timezone
import json
from corebase.rsa import encrypt, get_hash_sum, decrypt
import requests
from django.conf import settings


class AuthenticatorClient(object):

    def __init__(self, institution, url_notify):
        self.institution = institution
        self.url_notify = url_notify

    def authenticate(self, identification):

        data = {
            'institution': str(self.institution.code),
            'notification_url': self.url_notify.url or 'N/D',
            'identification': identification,
            'request_datetime': timezone.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
        algorithm = 'sha512'
        str_data = json.dumps(data)
        edata = encrypt(self.institution.server_public_key, str_data)
        hashsum = get_hash_sum(edata,  algorithm)
        edata = edata.decode()
        params = {
            "data_hash": hashsum,
            "algorithm": algorithm,
            "public_certificate": self.institution.public_certificate.decode(),
            'institution': str(self.institution.code),
            "data": edata,
        }
        result = requests.post(
            settings.UCR_FVA_SERVER_URL + '/authenticate/institution/', json=params)

        data = result.json()
        data = decrypt(self.institution.private_key, data['data'], as_str=True)

        return data
