
from django import forms
from institution.models import Institution

def get_institutions_names():
    return [('None', '------')]+list(Institution.objects.all().values_list('code', 'name'))

class StatForm(forms.Form):
    start_date = forms.DateTimeField()
    end_date = forms.DateTimeField()
    institution = forms.ChoiceField(
        choices=get_institutions_names, required=False)
    #transaction_success = forms.NullBooleanField()


    def to_dic_url(self):
        dev = {
            'start_date': self.cleaned_data['start_date'].strftime("%d/%m/%Y %H:%M:%S"),
            'end_date': self.cleaned_data['end_date'].strftime("%d/%m/%Y %H:%M:%S")
        }
        if self.cleaned_data['institution']:
            dev['institution'] = self.cleaned_data['institution']

        return dev

