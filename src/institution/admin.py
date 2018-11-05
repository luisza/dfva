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
@author: Luis Zarate Montero
@contact: luis.zarate@solvosoft.com
@license: GPLv3
'''

from django.conf import settings
from django.contrib import admin
from institution.models import NotificationURL, Institution
from institution.models import AuthenticateDataRequest, SignDataRequest, \
    ValidateCertificateDataRequest, ValidateDocumentDataRequest
# Register your models here.


class NotificationURLAdmin(admin.TabularInline):
    model = NotificationURL


class InstitutionAdmin(admin.ModelAdmin):
    inlines = [NotificationURLAdmin]


admin.site.register(Institution, InstitutionAdmin)

if settings.DEBUG:
    admin.site.register([
        AuthenticateDataRequest, SignDataRequest,
        ValidateCertificateDataRequest, ValidateDocumentDataRequest])
