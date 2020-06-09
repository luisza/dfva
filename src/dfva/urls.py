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
@date: 14/4/2017
@author: Universidad de Costa Rica
@maintainer: Luis Zarate Montero
@contact: luis.zarate@solvosoft.com
@license: GPLv3
'''

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

from django.views.generic import RedirectView
from django.urls import include, path, re_path
from django.contrib import admin
from django.conf import settings

urlpatterns = [
    path('', include('corebase.urls')),
    path('admin/', admin.site.urls),
]
if not settings.ONLY_BCCR:
    from rest_framework import routers
    from corebase.views import home
    from institution.urls import get_routes_view as instition_get_routes_view
    from person.urls import get_routes_view as person_get_routes_view
    from institution.urls import urlpatterns as institution_urls
    from django.contrib.auth.views import LoginView, LogoutView
    from django.urls.base import reverse_lazy

    router = routers.DefaultRouter()
    router.include_format_suffixes=False
    instition_get_routes_view(router)
    person_get_routes_view(router)



    urlpatterns += [
        path('', home, name="home"),
        path('accounts/login/', LoginView.as_view(),
            {'redirect_to': reverse_lazy("institution_list")}, name='login'),
        path('logout/', LogoutView.as_view(next_page=reverse_lazy('home')),  name='logout'),
        path('', include(router.urls)),
        path('', include('authorization_management.urls'))
    ] + institution_urls


from django.views.static import serve

urlpatterns += [
       re_path(r'^docs/?$', RedirectView.as_view(url='/docs/index.html')),
       re_path(r'^docs/(?P<path>.*)$', serve, {'document_root': settings.DOC_ROOT}),
       re_path(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),
       re_path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT})
]

