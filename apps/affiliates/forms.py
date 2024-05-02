
from django import forms
from .models import Contract, InsuranceRisk, Pollis

class ContractForm(forms.ModelForm):
    insurance_risk = forms.ModelMultipleChoiceField(queryset=InsuranceRisk.objects.all())
    
    class Meta:
        model = Contract
        fields = ('insurance_type', 'affiliate', 'insurance_object', 'insurance_risk',)
    
    def __init__(self, *args, **kwargs):
        super(ContractForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
                field.widget.attrs['class'] = 'form-control'


class PollisForm(forms.ModelForm):
    class Meta:
        model = Pollis
        exclude = ('agent',)
    
    def __init__(self, *args, **kwargs):
        super(PollisForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
                field.widget.attrs['class'] = 'form-control'