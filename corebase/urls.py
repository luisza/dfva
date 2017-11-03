# encoding: utf-8

'''
Created on 18 jul. 2017

@author: luisza
'''

from django.conf.urls import url


from pyfva.receptor.ws_service import ResultadoDeSolicitudSoap_SERVICE
from corebase.bccr_checks import soap_dispatcher
dispatcher = soap_dispatcher(ResultadoDeSolicitudSoap_SERVICE)



urlpatterns = [

    url(r'^wcfv2\/Bccr\.Sinpe\.Fva\.EntidadDePruebas\.Notificador\/ResultadoDeSolicitud\.asmx$',
        dispatcher, name='ws_receptor'),
]


