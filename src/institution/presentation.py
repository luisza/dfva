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
@date: 17/4/2017
@author: Luis Zarate Montero
@contact: luis.zarate@solvosoft.com
@license: GPLv3
'''

from __future__ import unicode_literals
from django.utils.safestring import mark_safe


class PEMpresentation(object):

    def present(self, data):
        if type(data) == bytes:
            data = data.decode()
        return mark_safe("<pre>%s</pre>" % (data))

    def get_private_key_display(self):
        return self.present(self.private_key)

    def get_public_key_display(self):
        return self.present(self.public_key)

    def get_public_certificate_display(self):
        return self.present(self.public_certificate)

    def get_server_sign_key_display(self):
        return self.present(self.server_sign_key)

    def get_server_public_key_display(self):
        return self.present(self.server_public_key)
