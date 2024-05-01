
from django import forms
from .models import Contract


class ContractForm(forms.ModelForm):
    class Meta:
        model = Contract
        fields = ('insurance_type', 'affiliate', )
    
    def __init__(self, *args, **kwargs):
        super(ContractForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
                field.widget.attrs['class'] = 'form-control'
        