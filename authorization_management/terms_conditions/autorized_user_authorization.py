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

from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.translation import gettext as _

from authorization_management.models import AuthorizationRequest


def authorize_user(request, user):
    authreq, created = AuthorizationRequest.objects.get_or_create(
        user=user,
        finished=False)
    if created:
        send_mail(
            _('Your request is pending'),
            _('Thanks, An authorized user will review your request and contact you soon.'),
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
            html_message=render_to_string(
                'mail/authorization_inproccess.html',
                {'object': authreq})
        )

    messages.success(request,
                     _("Congrats!, Your request was process successfully \
                     and will be review soon. You will get a confirmation \
                      email when your request is approved or denied"))
    return False
