'''
Created on 16 jun. 2018

@author: luis
'''
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from institution.models import Institution, NotificationURL


class InstitutionCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(InstitutionCreateForm, self).__init__(*args, **kwargs)

        # If you pass FormHelper constructor a form instance
        # It builds a default layout with all its fields
        self.helper = FormHelper(self)

        # You can dynamically adjust your layout
        self.helper.layout.append(Submit('save', 'save'))

    class Meta:
        model = Institution
        fields = ['name', 'email', 'phone', 'domain', 'institution_unit']


class InstitutionEditForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(InstitutionEditForm, self).__init__(*args, **kwargs)

        # If you pass FormHelper constructor a form instance
        # It builds a default layout with all its fields
        self.helper = FormHelper(self)

        # You can dynamically adjust your layout
        self.helper.layout.append(Submit('save', 'save'))

    class Meta:
        model = Institution
        fields = ['active', 'name', 'email', 'phone', 'domain',
                  'institution_unit', 'public_certificate', 'public_key']


class NotificationUrlsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(NotificationUrlsForm, self).__init__(*args, **kwargs)

        # If you pass FormHelper constructor a form instance
        # It builds a default layout with all its fields
        self.helper = FormHelper(self)

        # You can dynamically adjust your layout
        self.helper.layout.append(Submit('save', 'save'))

    class Meta:
        model = NotificationURL
        fields = ['description', 'url', 'not_webapp']
