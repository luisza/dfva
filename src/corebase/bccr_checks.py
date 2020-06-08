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
@date: 2/11/2017
@author: Universidad de Costa Rica
@maintainer: Luis Zarate Montero
@contact: luis.zarate@solvosoft.com
@license: GPLv3
'''

from django.conf import settings
from django.core.exceptions import DisallowedHost
from soapfish.django_ import django_dispatcher
from django.views.decorators.csrf import csrf_exempt

def check_ip(request):
    """Returns the IP of the request, accounting for the possibility of being
    behind a proxy.
    """
    allowed_ip = settings.ALLOWED_BCCR_IP
    if allowed_ip:
        ip = request.META.get("HTTP_X_FORWARDED_FOR", None)
        if ip:
            # X_FORWARDED_FOR returns client1, proxy1, proxy2,...
            ip = ip.split(", ")[0]
        else:
            ip = request.META.get("REMOTE_ADDR", "")
        if ip not in allowed_ip:
            raise DisallowedHost()


def soap_dispatcher(service, **dispatcher_kwargs):
    djdispatcher = django_dispatcher(service, **dispatcher_kwargs)

    def run(request, **kwargs):
        check_ip(request)
        response = djdispatcher(request, **kwargs)
        return  response
    return csrf_exempt(run)
