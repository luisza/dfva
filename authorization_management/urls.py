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
@date: 08/10/2018
@author: Luis Zarate Montero
@contact: luis.zarate@solvosoft.com
@license: GPLv3
'''

from django.conf.urls import url, include
from authorization_management.terms_conditions import sign_terms, \
    request_termsigned, sign_document_terms, check_autorization
from authorization_management.authentication import login_with_bccr,\
    consute_firma
from authorization_management.views import authorize_user_request

urlpatterns = [
    url(r'^authorize_user_terms', authorize_user_request,
        name="authorize_terms"),
    url(r"^autenticar$", login_with_bccr, name="login_fd"),
    url(r"^consute_firma$", consute_firma, name="consute_firma"),
    url(r'^sign_terms$', sign_terms, name='sign_terms'),
    url(r'^sign_terms_check$', request_termsigned, name="termsigned_check"),
    url(r'^sign_terms_document/(?P<pk>\d+)$',
        sign_document_terms, name="sign_terms_document"),
    url(r'^check_autorization$', check_autorization, name='check_autorization')
]
