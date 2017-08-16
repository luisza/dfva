'''
Created on 27 jul. 2017

@author: luis
'''
from django.utils import timezone
import json
from corebase.rsa import encrypt, get_hash_sum
import requests

from django.conf import settings


class SignerClient(object):
    def __init__(self, institution, url_notify):
        self.institution = institution
        self.url_notify = url_notify

    def sign(self, identification, document, resume, format='xml', algorithm='sha512'):

        data = {
            'institution': str(self.institution.code),
            'notification_url': self.url_notify.url or 'N/D',
            'document': document.decode(),
            'format': format,
            'algorithm_hash': algorithm,
            'document_hash': get_hash_sum(document,  algorithm),
            'identification': identification,
            'resumen': resume,
            'request_datetime': timezone.now().strftime("%Y-%m-%d %H:%M:%S"),
        }

        str_data = json.dumps(data)
        # print(str_data)
        edata = encrypt(self.institution.server_public_key, str_data)
        hashsum = get_hash_sum(edata,  algorithm)
        edata = edata.decode()
        params = {
            "data_hash": hashsum,
            "algorithm": algorithm,
            "public_certificate": self.institution.public_certificate,
            'institution': str(self.institution.code),
            "data": edata,
        }

        headers = {'Accept': 'application/json',
                   'Content-Type': 'application/json'}

        result = requests.post(
            settings.UCR_FVA_SERVER_URL + '/sign/institution/', json=params, headers=headers)

        # print(params)
        data = result.json()

        return data