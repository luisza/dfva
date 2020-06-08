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
from django.core.validators import URLValidator

from corebase.models import SUPPORTED_DOC_FORMAT
from institution.models import SignDataRequest
from django.utils.translation import ugettext_lazy as _


class SignDataForm(forms.ModelForm):
    document = forms.CharField()
    format = forms.CharField()
    algorithm_hash = forms.CharField()
    document_hash = forms.CharField()
    place = forms.CharField(max_length=150, required=False)
    reason = forms.CharField(max_length=125, required=False)
    notification_url = forms.CharField(max_length=200)
    resumen = forms.CharField(max_length=250, required=True)

    def clean(self):
        #FIXME: Eliminar comprobaciones extras en favor de forms
        cleaned_data = super().clean()
        if 'pdf' == format:
            if cleaned_data['place'] is None or cleaned_data['place'] == '':
                self.add_error('place', _("Place is required when you sign pdf documents"))
            if cleaned_data['reason'] is None or cleaned_data['reason'] == '':
                self.add_error('reason', _("Reason is required when you sign pdf documents"))

        if cleaned_data['format'].lower() not in SUPPORTED_DOC_FORMAT:
            self.add_error('format', _('Format not supported, supported formats are %s') % (
                    ", ".join(SUPPORTED_DOC_FORMAT)))
        #FIXME: Agregar validacion de comprobación de hash

    def clean_notification_url(self):
        data = self.cleaned_data['notification_url']
        if data.upper() != 'N/D':
            validator = URLValidator()
            validator(data)
        return data


    class Meta:
        model=SignDataRequest
        fields = ['institution', 'identification', 'request_datetime', 'document_hash']


class SignDataCheckForm(forms.ModelForm):
    notification_url = forms.CharField(max_length=200)

    def clean_notification_url(self):
        data = self.cleaned_data['notification_url']
        if data.upper() != 'N/D':
            validator = URLValidator()
            validator(data)
        return data

    class Meta:
        model=SignDataRequest
        fields = ['institution', 'request_datetime']