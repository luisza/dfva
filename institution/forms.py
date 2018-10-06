'''
Created on 16 jun. 2018

@author: luis
'''
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field
from institution.models import Institution, NotificationURL
from crispy_forms.bootstrap import Accordion, AccordionGroup


class InstitutionCreateForm(forms.ModelForm):
    bccr_negocio = forms.CharField(required=False)
    bccr_entidad = forms.CharField(required=False)

    def __init__(self, *args, **kwargs):
        super(InstitutionCreateForm, self).__init__(*args, **kwargs)

        # If you pass FormHelper constructor a form instance
        # It builds a default layout with all its fields
        self.helper = FormHelper(self)

        self.helper.layout = Layout(
            Accordion(
                AccordionGroup('General',
                               Field('name'),
                               Field('email'),
                               Field('phone'),
                               Field('domain'),
                               Field('institution_unit'),
                               active=True,

                               ),
                AccordionGroup('Avanzado',
                               Field('bccr_negocio'),
                               Field('bccr_entidad'),
                               active=False
                               )
            ),
            Submit('save', 'save')
        )

    def save(self, commit=True):
        changed = False
        obj = super(InstitutionCreateForm, self).save(commit=commit)
        negocio = self.cleaned_data.get('bccr_negocio', '')
        entidad = self.cleaned_data.get('bccr_entidad', '')
        if negocio:
            obj.bccr_bussiness = negocio
            changed = True
        if entidad:
            obj.bccr_entity = entidad
            changed = True
        if changed and commit:
            obj.save()
        return obj

    class Meta:
        model = Institution
        fields = ['name', 'email', 'phone', 'domain', 'institution_unit']


class InstitutionEditForm(forms.ModelForm):
    bccr_negocio = forms.CharField(required=False)
    bccr_entidad = forms.CharField(required=False)

    def __init__(self, *args, **kwargs):
        super(InstitutionEditForm, self).__init__(*args, **kwargs)

        # If you pass FormHelper constructor a form instance
        # It builds a default layout with all its fields
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Accordion(
                AccordionGroup('General',
                               Field('name'),
                               Field('active'),
                               Field('email'),
                               Field('phone'),
                               Field('domain'),
                               Field('institution_unit'),
                               Field('public_certificate'),
                               # Field('public_key'),

                               active=True,

                               ),
                AccordionGroup('Avanzado',
                               Field('bccr_negocio'),
                               Field('bccr_entidad'),
                               active=False
                               )
            ),
            Submit('save', 'save')
        )

    def save(self, commit=True):
        changed = False
        obj = super(InstitutionEditForm, self).save(commit=commit)
        negocio = self.cleaned_data.get('bccr_negocio', '')
        entidad = self.cleaned_data.get('bccr_entidad', '')
        print("BINGO: ", negocio, entidad)
        if negocio:
            obj.bccr_bussiness = negocio
            changed = True
        if entidad:
            obj.bccr_entity = entidad
            changed = True
        if changed and commit:
            obj.save()
        return obj

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
