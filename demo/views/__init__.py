from demo.forms import AuthenticateForm, SignForm, ValidateForm
from django.shortcuts import render


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
