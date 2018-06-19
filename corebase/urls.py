# encoding: utf-8

'''
Created on 18 jul. 2017

@author: luisza
'''

from django.conf.urls import url


from pyfva.receptor.ws_service import ResultadoDeSolicitudSoap_SERVICE
from corebase.bccr_checks import soap_dispatcher
from corebase.authentication import login_with_bccr, consute_firma
from corebase.terms_conditions import sign_terms, request_termsigned,\
    sign_document_terms, check_autorization
dispatcher = soap_dispatcher(ResultadoDeSolicitudSoap_SERVICE)


urlpatterns = [

    url(r'^wcfv2\/Bccr\.Sinpe\.Fva\.EntidadDePruebas\.Notificador\/ResultadoDeSolicitud\.asmx$',
        dispatcher, name='ws_receptor'),
    url(r"^autenticar$", login_with_bccr, name="login_fd"),
    url(r"^consute_firma$", consute_firma, name="consute_firma"),
    url(r'^sign_terms$', sign_terms, name='sign_terms'),
    url(r'^sign_terms_check$', request_termsigned, name="termsigned_check"),
    url(r'^sign_terms_document/(?P<pk>\d+)$',
        sign_document_terms, name="sign_terms_document"),
    url(r'^check_autorization$', check_autorization, name='check_autorization')
]
