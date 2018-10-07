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

from person.authenticator.views import AuthenticatePersonRequestViewSet
from person.signer.views import SignPersonRequestViewSet
from person.validator.views import ValidatePersonViewSet,\
    ValidateSubscriptorPersonViewSet
from person.views import PersonLoginView


def get_routes_view(router):
    router.register(r'authenticate', AuthenticatePersonRequestViewSet)
    router.register(r'sign', SignPersonRequestViewSet)
    router.register(r'validate', ValidatePersonViewSet)
    router.register(r'validate', ValidateSubscriptorPersonViewSet)
    router.register(r'login', PersonLoginView)
