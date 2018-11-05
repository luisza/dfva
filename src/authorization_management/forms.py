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
@date: 18/7/2018
@author: Luis Zarate Montero
@contact: luis.zarate@solvosoft.com
@license: GPLv3
'''

from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.contrib.auth.models import User
from authorization_management.models import UserConditionsAndTerms
from django.urls.base import reverse
from django.utils.translation import gettext as _


class RegistationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(RegistationForm, self).__init__(*args, **kwargs)

        # If you pass FormHelper constructor a form instance
        # It builds a default layout with all its fields
        self.helper = FormHelper(self)

        # You can dynamically adjust your layout
        self.helper.layout.append(Submit('save', _('Continue')))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class UserConditionsAndTermsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(UserConditionsAndTermsForm, self).__init__(*args, **kwargs)

        # If you pass FormHelper constructor a form instance
        # It builds a default layout with all its fields
        self.helper = FormHelper(self)
        # You can dynamically adjust your layout
        self.helper.layout.append(Submit('save', _('Continue')))
        self.helper.form_action = reverse('sign_terms')

    class Meta:
        model = UserConditionsAndTerms
        fields = ['organization', 'organization_unit',
                  'use_reason', 'phone']
