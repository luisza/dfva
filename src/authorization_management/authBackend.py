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
@date: 7/8/2018
@author: Luis Zarate Montero
@contact: luis.zarate@solvosoft.com
@license: GPLv3
'''

from django.contrib.auth.models import User
from institution.models import AuthenticateDataRequest
from django.conf import settings


class DFVABackend(object):

    def authenticate(self, token=None):
        Rauth = AuthenticateDataRequest.objects.filter(
            id_transaction=token).first()
        if Rauth and Rauth.received_notification and \
                Rauth.status == settings.DEFAULT_SUCCESS_BCCR:
            try:
                user = User.objects.get(username=Rauth.identification)
            except User.DoesNotExist:
                # Create a new user. There's no need to set a password
                # because only the password from settings.py is checked.
                user = User(username=Rauth.identification)
                user.is_staff = False
                user.is_superuser = False
                user.save()
            return user
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
