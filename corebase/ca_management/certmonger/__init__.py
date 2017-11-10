'''
Created on 27 oct. 2017

apt-get install libsasl2-dev python3-dev libldap2-dev libssl-dev
apt-get install krb5-config libkrb5-dev
* puede que krb5-config no sea necesario para pruebas

Reino predeterminado de la versión 5 de Kerberos:  DFVA.CR
Introduzca los nombres de los servidores Kerberos en el reino DFVA.CR de Kerberos, separados por espacios.  kbr.dfva.cr

@author: luis
'''
"""
from corebase.ca_management.interface import CAManagerInterface
from ipapython.certmonger import get_request_value, stop_tracking, request_cert
from ipaplatform.paths import paths


class CAManager(CAManagerInterface):
    def generate_certificate(self, domain, save_model):
            request_id = request_cert(paths.HTTPD_ALIAS_DIR, "Test",
                              "cn="+domain+",C=CR,ST=San Jose,L=Costa Rica,O="save_model.name+",OU="+save_model.institution_unit
                              "HTTP/dfva@dfva.cr")
    csr = get_request_value(request_id, 'csr')
    print(csr)
    stop_tracking(request_id)
    
    def check_certificate(self, certificate):
        pass

    def revoke_certificate(self, certificate):
        pass

"""
