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

from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext as _


class AuthorizationRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    request_date = models.DateTimeField(auto_now_add=True)
    last_modification = models.DateTimeField(auto_now=True)
    authorized = models.BooleanField(default=False)
    finished = models.BooleanField(default=False)
    who_authorized = models.ForeignKey(User, related_name="who_authorized",
                                       null=True, blank=True, on_delete=models.DO_NOTHING)
    observations = models.TextField(null=True, blank=True)

    @property
    def terms_and_conditions(self):
        return UserConditionsAndTerms.objects.get(user=self.user)

    def __str__(self):
        status = _("Denied or in check")
        if self.autorized:
            status = _("Authorized")
        return self.user.username + " ( "+status+" )"

    class Meta:
        verbose_name = _('Authorization request')
        verbose_name_plural = _('Authorizations request')


class UserConditionsAndTerms(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    document_signed = models.TextField()
    signed = models.BooleanField(default=False)

    organization = models.CharField(max_length=100)
    organization_unit = models.CharField(max_length=100)
    use_reason = models.TextField(
        help_text=_("Why we have to allow you to use this digital \
        signer service?"))

    phone = models.CharField(max_length=25)
    contact_email = models.EmailField()

    def __str__(self):
        return "%s %s (signed %s)" % (self.user.username,
                                      self.organization, self.signed)
