'''
Created on 4 mar. 2018

@author: luisza
'''
from django.conf import settings

def get_requests_ssl_context():
    kwargs={}
    requests_ca_check = getattr(settings, 'DFVA_CA_CHECK', None)
    requests_ca =  getattr(settings, 'DFVA_CA_PATH', '')
    requests_cert = getattr(settings, 'DFVA_CERT_PATH', '')
    requests_key = getattr(settings, 'DFVA_KEY_PATH', '')    
        
    if requests_ca and requests_ca_check:
        kwargs['verify'] = requests_ca
    if requests_ca_check is False:
        kwargs['verify'] = requests_ca_check
    if requests_cert and requests_key:
        kwargs['cert']=(requests_cert, requests_key)
    elif requests_cert:
        kwargs['cert']=requests_cert
    return kwargs