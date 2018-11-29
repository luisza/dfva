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
@date: 4/3/2018
@author: Universidad de Costa Rica
@maintainer: Luis Zarate Montero
@contact: luis.zarate@solvosoft.com
@license: GPLv3
'''

from django.conf import settings


def get_requests_ssl_context():
    kwargs = {}
    requests_ca_check = getattr(settings, 'DFVA_CA_CHECK', None)
    requests_ca = getattr(settings, 'DFVA_CA_PATH', '')
    requests_cert = getattr(settings, 'DFVA_CERT_PATH', '')
    requests_key = getattr(settings, 'DFVA_KEY_PATH', '')

    if requests_ca and requests_ca_check:
        kwargs['verify'] = requests_ca
    if requests_ca_check is False:
        kwargs['verify'] = requests_ca_check
    if requests_cert and requests_key:
        kwargs['cert'] = (requests_cert, requests_key)
    elif requests_cert:
        kwargs['cert'] = requests_cert
    return kwargs
