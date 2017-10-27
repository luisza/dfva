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
from rest_framework import routers
from django.conf import settings
from institution.urls import get_routes_view as instition_get_routes_view
from person.urls import get_routes_view as person_get_routes_view
from institution.urls import urlpatterns as institution_urls

router = routers.DefaultRouter()
instition_get_routes_view(router)
person_get_routes_view(router)


urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name="index.html")),
    url(r'^accounts/login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, name='logout'),
    url(r'^admin/', admin.site.urls),
    url(r'^select2/', include('django_select2.urls')),
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework')),
    url(r'^', include('corebase.urls')),
    url(r'^', include(router.urls)),
] + institution_urls

if settings.DEMO:
    # IF DEMO, remove in production
    from demo.urls import urlpatterns as demourls
    urlpatterns += demourls
