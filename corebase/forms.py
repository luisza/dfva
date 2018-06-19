'''
Created on 18 jun. 2018

@author: luis
'''
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.contrib.auth.models import User
from corebase.models import UserConditionsAndTerms
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
