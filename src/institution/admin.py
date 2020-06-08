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

from django.conf import settings
from django.contrib import admin

from corebase.admin_utils import CsvExporter
from institution.models import NotificationURL, Institution, InstitutionStats
from institution.models import AuthenticateDataRequest, SignDataRequest, \
    ValidateCertificateDataRequest, ValidateDocumentDataRequest
# Register your models here.


class NotificationURLAdmin(admin.TabularInline):
    model = NotificationURL


class InstitutionAdmin(admin.ModelAdmin):
    inlines = [NotificationURLAdmin]


class InstitutionStatsAdmin(CsvExporter, admin.ModelAdmin):
    list_display = (
    'institution',
    'datetime',
    'status',
    'notified',
    'transaction_id',
    'data_type',
    'document_type',
    'was_successfully'

    )
    actions = ["export_as_csv"]
    csv_field_names = ['institution',
    'datetime',
    'status',
    'notified',
    'transaction_id',
    'data_type',
    'document_type',
    'was_successfully']

admin.site.register(InstitutionStats, InstitutionStatsAdmin)

admin.site.register(Institution, InstitutionAdmin)

if settings.DEBUG_LAST_REQUESTS:
    admin.site.register([
        AuthenticateDataRequest, SignDataRequest,
        ValidateCertificateDataRequest, ValidateDocumentDataRequest])
