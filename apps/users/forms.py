
from django import forms

from .mixins import ValidationMixin
from .models import Agent, Client, CustomUser, Feedback


class RegistrationForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name',)


class UpdateForm(forms.ModelForm, ValidationMixin):
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'gender', 'age', 'profile_image',)

 
class ClientRegistrationForm(forms.ModelForm, ValidationMixin):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Client
        exclude = ('address', 'phone', 'user', 'balance',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.update(RegistrationForm().fields)
        self.order_fields(['email', 'first_name', 'last_name', 'password1', 'password2'])


    def clean(self):
        self.check_email(self.cleaned_data.get('email'))
        self.check_passwords(self.cleaned_data.get('password1'), self.cleaned_data.get('password2'))

    
class AgentRegistrationForm(forms.ModelForm, ValidationMixin):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = Agent
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.update(RegistrationForm().fields)
    
    def clean(self):
        self._clean_email(self.cleaned_data.get('email'))
        self._clean_passwords(self.cleaned_data.get('password1'), self.cleaned_data.get('password2'))


class LoginForm(forms.Form):
    class Meta:
        model = CustomUser
        fields = ('email', 'password',)

    email = forms.CharField(max_length=255)
    password = forms.CharField(max_length=255, widget=forms.PasswordInput)


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = '__all__'

class ClientUpdateForm(forms.ModelForm, ValidationMixin):
    class Meta:
        model = Client
        fields = ('address', 'phone',)

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields.update(UpdateForm().fields)
        if user:
            self.initial.update({
                'profile_image': user.profile_image,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'gender': user.gender,
                'age': user.age
            })
    
    def clean(self):
        self.check_age(self.cleaned_data.get('age'))


class AgentUpdateForm(forms.ModelForm, ValidationMixin):
    class Meta:
        model = Agent
        exclude = ('user', 'affiliate', 'salary', 'tariff_rate')

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields.update(UpdateForm().fields)
        if user:
            self.initial.update({
                'profile_image': user.profile_image,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'gender': user.gender,
                'age': user.age
            })
            

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        exclude = ('client',)
            

class BalanceForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ('balance',)
