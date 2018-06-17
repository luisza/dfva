# encoding: utf-8

'''
Created on 18 jul. 2017

@author: luisza
'''

from django.conf.urls import url


from pyfva.receptor.ws_service import ResultadoDeSolicitudSoap_SERVICE
from corebase.bccr_checks import soap_dispatcher
from corebase.authentication import login_with_bccr, consute_firma
dispatcher = soap_dispatcher(ResultadoDeSolicitudSoap_SERVICE)


urlpatterns = [

    url(r'^wcfv2\/Bccr\.Sinpe\.Fva\.EntidadDePruebas\.Notificador\/ResultadoDeSolicitud\.asmx$',
        dispatcher, name='ws_receptor'),
    url(r"^autenticar$", login_with_bccr, name="login_fd"),
    url(r"^consute_firma$", consute_firma, name="consute_firma")
]
