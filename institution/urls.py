'''
Created on 12 sep. 2017

@author: luisza
'''
from institution.authenticator.views import AuthenticateRequestViewSet
from institution.signer.views import SignRequestViewSet
from institution.validator.views import ValidateInstitutionViewSet,\
    ValidateSubscriptorInstitutionViewSet

from django.conf.urls import include, url
from institution import views
from institution.views.graphs import get_institution_stats


def get_routes_view(router):
    router.register(r'authenticate', AuthenticateRequestViewSet)
    router.register(r'sign', SignRequestViewSet)
    router.register(r'validate', ValidateInstitutionViewSet)
    router.register(r'validate', ValidateSubscriptorInstitutionViewSet)


urlpatterns = [
    url(r"^institution/create$", views.CreateInstitution.as_view(),
        name="institution_create"),
    url(r"^institution/(?P<pk>[0-9A-Fa-f-]+)/edit$", views.EditInstitution.as_view(),
        name="institution_edit"),
    url(r"institution/list", views.ListInstitution.as_view(),
        name="institution_list"),
    url(r"institution/(?P<pk>[0-9A-Fa-f-]+)/detail$", views.InstitutionDetail.as_view(),
        name="institution_show"),
    url(r"institution/(?P<pk>[0-9A-Fa-f-]+)/delete$", views.DeleteInstitution.as_view(),
        name="institution_delete"),
    url(r"keys/(?P<pk>[0-9A-Fa-f-]+)/new",
        views.get_new_certificates, name="new_institution_keys"),
    url(r"notificationurls/(?P<pk>[0-9A-Fa-f-]+)/(?P<nu>\d+)?$",
        views.manage_notificationurls, name="notification_urls"),

    url(r'institution/(?P<pk>[0-9A-Fa-f-]+)/stats$',
        get_institution_stats, name="institution_stats")
]
