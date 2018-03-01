'''
Created on 26 jul. 2017

@author: luis
'''


from django import forms
from base64 import b64encode
from demo.clientes.authenticator import AuthenticatorClient
from demo.clientes.signer import SignerClient
from demo.clientes.validator import ValidatorClient
from institution.models import NotificationURL


class AuthenticateForm(forms.Form):
    url = forms.ModelChoiceField(queryset=NotificationURL.objects.filter(is_demo=True))
    identificacion = forms.CharField(max_length=16, min_length=11)

    def send(self):

        url = self.cleaned_data['url']
        identification = self.cleaned_data['identificacion']
        client = AuthenticatorClient(
            url.institution,
            url
        )
        return client.authenticate(identification)


class SignForm(forms.Form):
    url = forms.ModelChoiceField(queryset=NotificationURL.objects.filter(is_demo=True))
    identificacion = forms.CharField(max_length=16, min_length=11)
    documento = forms.FileField()
    formato = forms.ChoiceField(choices=(
        ('xml_cofirma', 'XML Cofirma'),
        ('xml_contrafirma', 'XML Contra firma'),
        ('odf', 'ODF'),
        ('msoffice', 'Microsoft Office'),
        ("pdf", "PDF")
        ),
        initial='xml_cofirma')
    algoritmo = forms.ChoiceField(choices=(
        ('Sha256', 'sha256'),
        ('Sha384', 'sha384'),
        ('Sha512', 'sha512')),
        initial='Sha512')

    resume = forms.CharField()

    def send(self):
        url = self.cleaned_data['url']
        client = SignerClient(
            url.institution,
            url
        )
        dev = client.sign(self.cleaned_data['identificacion'],
                          b64encode(self.cleaned_data['documento'].read()),
                          self.cleaned_data['resume'],
                          format=self.cleaned_data['formato'],
                          algorithm=self.cleaned_data['algoritmo'].lower())
        return dev


class ValidateForm(forms.Form):
    url = forms.ModelChoiceField(queryset=NotificationURL.objects.filter(is_demo=True))
    documento = forms.CharField(widget=forms.Textarea)
    tipo = forms.ChoiceField(choices=(
        ('documento', 'Documento'),
        ('certificado', 'Certificado'),
    ), initial='documento')
    formato = forms.ChoiceField(choices=(
        ('cofirma', 'XML Cofirma'),
        ('contrafirma', 'XML Contra firma'),
        ('odf', 'ODF'),
        ('msoffice', 'Microsoft Office'),
        ("pdf", "pdf")
        ),
        initial='cofirma')

    def send(self):
        url = self.cleaned_data['url']
        client = ValidatorClient(
            url.institution,
            url
        )

        dev = client.validate(
            self.cleaned_data['documento'],
            self.cleaned_data['tipo'],
            self.cleaned_data['formato']
        )
        return dev
