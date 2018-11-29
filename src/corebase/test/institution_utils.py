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
@date: 15/8/2017
@author: Universidad de Costa Rica
@maintainer: Luis Zarate Montero
@contact: luis.zarate@solvosoft.com
@license: GPLv3
'''

from corebase.ca_management import create_certiticate
from institution.models import Institution, NotificationURL


def create_institution(user, domain='dfva.cr',
                       name="test institution",
                       institution_unit='QA'):
    save_model = Institution(
        user=user,
        name=name,
        active=True,
        domain=domain,
        institution_unit=institution_unit)
    create_certiticate(domain, save_model)
    save_model.save()

    return save_model


def create_url(institution, url='N/D', description="test url", is_demo=False):
    return NotificationURL.objects.create(
        description=description,
        url=url,
        institution=institution,
        not_webapp=url == 'N/D',
        is_demo=is_demo
    )
