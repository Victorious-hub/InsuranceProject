
from datetime import datetime
from typing import Any
from django import forms
from .models import Contract, InsuranceRisk, Policy

class ContractForm(forms.ModelForm):
    insurance_risk = forms.ModelMultipleChoiceField(queryset=InsuranceRisk.objects.all())
    
    class Meta:
        model = Contract
        fields = ('insurance_type', 'affiliate', 'insurance_object', 'insurance_risk',)
    

class PolicyForm(forms.ModelForm):
    class Meta:
        model = Policy
        exclude = ('agent', 'created_at')
    
    def __init__(self, *args, **kwargs):
        super(PolicyForm, self).__init__(*args, **kwargs)
        self.fields['start_date'].widget = forms.widgets.DateInput(
            attrs={
                'type': 'date', 'placeholder': 'yyyy-mm-dd (DOB)',
                'class': 'form-control'
                }
            )
        self.fields['end_date'].widget = forms.widgets.DateInput(
            attrs={
                'type': 'date', 'placeholder': 'yyyy-mm-dd (DOB)',
                'class': 'form-control'
                }
            )
    
    def clean(self):
        if self.cleaned_data.get('start_date') > self.cleaned_data.get('end_date'):
            raise forms.ValidationError("End date must be greater than start date")
        if self.cleaned_data.get('start_date') < datetime.now().date():
            raise forms.ValidationError("Start date must be greater than today")
        if self.cleaned_data.get('insurance_sum') <= 0 or self.cleaned_data.get('price') <= 0:
            raise forms.ValidationError("Insurance sum or price must be greater than 0")
        return self.cleaned_data