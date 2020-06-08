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

from institution.models import AuthenticateDataRequest
from django.core.validators import URLValidator


class AuthenticateForm(forms.ModelForm):
    notification_url = forms.CharField(max_length=400)

    def clean_notification_url(self):
        data = self.cleaned_data['notification_url']
        if data.upper() != 'N/D':
            validator = URLValidator()
            validator(data)
        return data

    class Meta:
        model = AuthenticateDataRequest
        fields = ['identification', 'request_datetime', 'institution']


class AuthenticateCheckForm(forms.ModelForm):
    notification_url = forms.CharField(max_length=400)

    def clean_notification_url(self):
        data = self.cleaned_data['notification_url']
        if data.upper() != 'N/D':
            validator = URLValidator()
            validator(data)
        return data

    class Meta:
        model = AuthenticateDataRequest
        fields = ['request_datetime', 'institution']
