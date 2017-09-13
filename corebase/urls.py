# encoding: utf-8

'''
Created on 18 jul. 2017

@author: luisza
'''

from django.conf.urls import url

from soapfish.django_ import django_dispatcher
from pyfva.receptor.ws_service import ResultadoDeSolicitudSoap_SERVICE
dispatcher = django_dispatcher(ResultadoDeSolicitudSoap_SERVICE)



urlpatterns = [

    url(r'^wcfv2\/Bccr\.Sinpe\.Fva\.EntidadDePruebas\.Notificador\/ResultadoDeSolicitud\.asmx$',
        dispatcher, name='ws_receptor'),
]


