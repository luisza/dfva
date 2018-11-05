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

from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, render
from django.template.loader import render_to_string
from django.utils.translation import gettext as _
from authorization_management.models import AuthorizationRequest
from authorization_management.utils import authorize_user_to_create_institution
from django.conf import settings


@login_required
@permission_required('authorization_management.change_authorizationrequest')
def authorize_user_request(request):

    if request.method == 'POST':
        auth = get_object_or_404(AuthorizationRequest,
                                 pk=request.POST.get('authrequest', '0'))
        status = request.POST.get('status', '')
        observations = request.POST.get('observations', '')
        if status in ['approve', "disapprove"]:
            auth.authorized = 'approve' == status
            auth.finished = True
            auth.who_authorized = request.user
            auth.observations = observations
            auth.save()
            messages.success(request,
                             _("Thanks, authorization was successfully saved"))

            if auth.authorized:
                authorize_user_to_create_institution(auth.user)
            send_mail(
                _('Your request was updated'),
                'The status of %s is %s' % (
                    auth.user.username, auth.authorized),
                settings.DEFAULT_FROM_EMAIL,
                [auth.user.email],
                fail_silently=False,
                html_message=render_to_string(
                    'mail/authorization_process.html',
                    {'object': auth,
                     'is_authorized': _('Approved') if auth.authorized
                     else _('Disapproved'),
                     'who_authorized': request.user})
            )

        else:
            messages.error(request,
                           _("Sorry Unknown status"))
    objs = AuthorizationRequest.objects.filter(
        finished=False
    )
    return render(
        request,
        'authorization_request.html',
        {'object_list': objs}
    )
