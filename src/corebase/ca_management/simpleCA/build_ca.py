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
@date: 10/9/2018
@author: Universidad de Costa Rica
@maintainer: Luis Zarate Montero
@contact: luis.zarate@solvosoft.com
@license: GPLv3
'''

from django.conf import settings
from oscrypto import asymmetric
from certbuilder import CertificateBuilder, pem_armor_certificate
from crlbuilder import CertificateListBuilder
from django.utils import timezone
from datetime import timedelta
import os


def build_ca():
    if not os.path.exists(settings.CA_PATH):
        os.makedirs(settings.CA_PATH)

    root_ca_public_key, root_ca_private_key = asymmetric.generate_pair(
        'rsa', bit_size=4096)

    with open(settings.CA_KEY, 'wb') as f:
        f.write(asymmetric.dump_private_key(
            root_ca_private_key, settings.CA_KEY_PASSWD))

    builder = CertificateBuilder(
        {
            'country_name': 'CR',
            'state_or_province_name': 'San Jose',
            'locality_name': 'Costa Rica',
            'organization_name': 'DFVA Independiente',
            'common_name': 'DFVA Root CA 1',
        },
        root_ca_public_key
    )
    now = timezone.now()
    builder.self_signed = True
    builder.ca = True
    builder.end_date = now+timedelta(settings.CA_CERT_DURATION*10)
    root_ca_certificate = builder.build(root_ca_private_key)

    with open(settings.CA_CERT, 'wb') as f:
        f.write(pem_armor_certificate(root_ca_certificate))

    builder = CertificateListBuilder(
        'http://crl.dfva.info',
        root_ca_certificate,
        1000
    )
    crl_list = builder.build(root_ca_private_key)

    with open(settings.CA_CRL, 'wb') as f:
        f.write(crl_list.dump())
