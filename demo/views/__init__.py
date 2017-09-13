from demo.forms import AuthenticateForm, SignForm, ValidateForm
from django.shortcuts import render
from cruds_adminlte.crud import CRUDView
from django import forms
from django.contrib.auth.models import User
from person.models import Person


def show_simulate_bccr_request(request, nform):
    forms = {
        'auth': AuthenticateForm,
        'sign': SignForm,
        'validate': ValidateForm,
    }

    titles = {
        'auth': "Autenticación",
        'sign': "Firma de documentos",
        'validate': "Validación de documentos y certificados",
        'verify': "Verificación de la firma completa"

    }

    form = forms[nform]
    message = None
    if request.method == 'POST':
        form = form(request.POST, request.FILES)
        if form.is_valid():
            data = form.send()
            form = forms[nform]()
            message = "Request sended successfully returned %r" % (data, )

    else:
        form = form()

    return render(request, 'simulate_bccr_request.html', {'form': form,
                                                          'title': titles[nform],
                                                          'message': message})


class PersonForm(forms.ModelForm):
    email = forms.EmailField()
    first_name = forms.CharField()
    last_name = forms.CharField()

    def save(self, commit=False):
        obj = super(PersonForm, self).save(commit=False)
        user = User.objects.create_user(self.cleaned_data['identification'],
                                        email=self.cleaned_data['email']
                                        )
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()
        obj.user = user
        obj.save()
        return obj

    class Meta:
        model = Person
        fields = ['identification']


class PersonView(CRUDView):
    model = Person
    views_available = ['create', 'list', 'delete']
    update_form = PersonForm
    add_form = PersonForm
    list_fields = ['identification']
