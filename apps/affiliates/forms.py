
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