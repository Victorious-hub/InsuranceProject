
from django import forms
from .models import Contract


class ContractForm(forms.ModelForm):
    class Meta:
        model = Contract
        fields = ('client', 'insurance_type', 'insurance_sum', 'start_date', 'end_date',)
        