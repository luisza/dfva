# encoding: utf-8

'''
Created on 18 jul. 2017

@author: luisza
'''

from django.conf.urls import url, include
from .views import InstitutionCRUD

from soapfish.django_ import django_dispatcher
from pyfva.receptor.ws_service import ResultadoDeSolicitudSoap_SERVICE
from corebase.views import PersonLoginView

dispatcher = django_dispatcher(ResultadoDeSolicitudSoap_SERVICE)


def get_routes_view(router):
    router.register(r'login', PersonLoginView)
    # pass


urlpatterns = [

    url(r'^wcfv2\/Bccr\.Sinpe\.Fva\.EntidadDePruebas\.Notificador\/ResultadoDeSolicitud\.asmx$',
        dispatcher, name='ws_receptor'),
]

try:
    # FIXME: crash when migrations are not applied
    iviews = InstitutionCRUD()

    urlpatterns += [
        url(r'^', include(iviews.get_urls())),
    ]
except:
    pass
