"""dfva URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.views.generic.base import TemplateView
from rest_framework.documentation import include_docs_urls
from rest_framework import routers
from authenticator.urls import get_routes_view as auth_routes_view
from signer.urls import get_routes_view as sign_routes_view
from validator.urls import get_routes_view as validate_routes_view
from pyfva.receptor.ws_service import ResultadoDeSolicitudSoap_SERVICE
from soapfish.django_ import django_dispatcher
dispatcher = django_dispatcher(ResultadoDeSolicitudSoap_SERVICE)
from django.conf import settings

router = routers.DefaultRouter()
auth_routes_view(router)
sign_routes_view(router)
validate_routes_view(router)


urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name="index.html")),
    url(r'^accounts/login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, name='logout'),
    url(r'^admin/', admin.site.urls),
    url(r'^select2/', include('django_select2.urls')),
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework')),
    url(r'^docs/',
        include_docs_urls(title='API de Dfva')),
    url(r'^', include('corebase.urls')),
    url(r'^', include(router.urls)),
]

if settings.DEMO:
    # IF DEMO, remove in production
    from demo.urls import urlpatterns as demourls
    urlpatterns += demourls
