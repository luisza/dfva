# encoding: utf-8

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

'''
@date: 12/9/2017
@author: Luis Zarate Montero
@contact: luis.zarate@solvosoft.com
@license: GPLv3
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
    url(r"notificationurls/(?P<pk>\d+)/delete$",
        views.delete_notificationurls, name="del_notification_urls"),
    url(r'institution/(?P<pk>[0-9A-Fa-f-]+)/stats$',
        get_institution_stats, name="institution_stats")
]
