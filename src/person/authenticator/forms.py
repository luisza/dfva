from django import forms

from person.models import AuthenticatePersonDataRequest


class AuthenticateForm(forms.ModelForm):

    class Meta:
        model = AuthenticatePersonDataRequest
        fields = ['identification', 'request_datetime']

