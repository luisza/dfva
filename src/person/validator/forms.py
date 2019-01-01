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
@date: 31/12/2018
@author: Universidad de Costa Rica
@maintainer: Luis Zarate Montero
@contact: luis.zarate@solvosoft.com
@license: GPLv3
'''

from django import forms

from corebase.models import SUPPORTED_DOC_FORMAT
from person.models import ValidatePersonCertificateDataRequest, ValidatePersonDocumentDataRequest
from django.utils.translation import ugettext_lazy as _


class ValidatePersonCertificateDataForm(forms.ModelForm):
    document = forms.CharField()

    class Meta:
        model = ValidatePersonCertificateDataRequest
        fields = ['person',   'request_datetime']


class ValidatePersonDocumentDataForm(forms.ModelForm):
    document = forms.CharField()

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data['format'].lower() not in dict(ValidatePersonDocumentDataRequest.FORMATS):
            self.add_error('format', _('Format not supported, supported formats are %s') % (
                    ", ".join(list(dict(SUPPORTED_DOC_FORMAT)).keys())))
    class Meta:
        model = ValidatePersonDocumentDataRequest
        fields = ['person',   'format', 'request_datetime']