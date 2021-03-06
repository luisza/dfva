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
@date: 8/10/2018
@author: Luis Zarate Montero
@contact: luis.zarate@solvosoft.com
@license: GPLv3
'''

from django.contrib.auth.models import Group
from django.conf import settings


def authorize_user_to_create_institution(user):
    """
    Agrega un usuario al grupo de usuarios autorizados

    :param user: Usuario a autorizar
    :return:  None
    """
    group = Group.objects.get(name=settings.INSTITUTION_GROUP_NAME)
    user.groups.add(group)
