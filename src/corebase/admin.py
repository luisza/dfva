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

from django.contrib import admin

from corebase.admin_utils import CsvExporter
from corebase.models import System_Request_Metric, BCCR_Monitor



class AdminMetrics(CsvExporter, admin.ModelAdmin):
    list_display = ('operation_type', 'transaction_status',
                    #'transaction_status_text',
                   'check_institution_certificate', 'decrypt_time', 'bccr_call', 'save_database',
                    'encrypt_time', 'total_spend_time')
    actions = ["export_as_csv"]
    date_hierarchy = 'end_decrypt'
    csv_field_names = [
        'operation_type',
        'transaction_status',
        'transaction_status_text',
        'transaction_success',
        # Spent time
        'check_institution_certificate',
        'decrypt_time',
        'bccr_call',
        'save_database',
        'encrypt_time',
        'total_spend_time',
        # datetime metric
        'start_bccr_call',
        'end_bccr_call',
        'start_save_database',
        'end_save_database',
        'start_check_institution_certificate',
        'end_check_institution_certificate',
        'start_decrypt',
        'end_decrypt',
        'start_encryption',
        'end_encryption',
        'start_hashsum',
        'end_hashsum'
    ]


class AdminBccrMonitor(CsvExporter, admin.ModelAdmin):
    list_display = ('medition_time', 'authenticate',
                    'signer', 'validate_certificate', 'validate_document', 'everything_ok' )
    actions = ["export_as_csv"]
    date_hierarchy = 'medition_time'
    csv_field_names = ['medition_time', 'medition_time', 'authenticate',
                        'signer', 'validate_certificate', 'validate_document', 'everything_ok']

admin.site.register(BCCR_Monitor, AdminBccrMonitor)
admin.site.register(System_Request_Metric, AdminMetrics)
