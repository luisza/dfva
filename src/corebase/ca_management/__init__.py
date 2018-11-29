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

from __future__ import unicode_literals

from django.conf import settings

from importlib import import_module

if hasattr(settings, 'CAMANAGER_CLASS'):
    CAManager = import_module(settings.CAMANAGER_CLASS).CAManager
else:
    from corebase.ca_management.simpleCA import CAManager

CA_manag_instance = CAManager()
# When dogtag module is done this has sense
if hasattr(settings, 'USE_DOCTAG'):
    pass


def create_certiticate(domain, save_model):
    return CA_manag_instance.generate_certificate(domain, save_model)


def check_certificate(certificate):
    return CA_manag_instance.check_certificate(certificate)


def revoke_certificate(certificate):
    return CA_manag_instance.revoke_certificate(certificate)
