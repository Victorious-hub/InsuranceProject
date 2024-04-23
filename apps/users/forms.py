
from django.contrib.auth.forms import UserCreationForm
from django import forms

from .models import Agent, Client, CustomUser

class ClientRegisterForm(UserCreationForm):
    class Meta:
        model = Client
        fields = ('gender','first_name', 'last_name', 'email', 'address', 'phone',)
    
    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password2'] != cd['password1']:
            raise forms.ValidationError("Password don't match")

        return cd['password2']

    
# class AgentRegisterForm(UserCreationForm):
#     class Meta:
#         model = Agent
#         fields = '__all__'

#     user = CustomUserForm()

#     def __init__(self, *args, **kwargs):
#         super(AgentRegisterForm, self).__init__(*args, **kwargs)
#         self.fields['user'].widget.attrs['class'] = 'form-control'
