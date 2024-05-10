
from django import forms
from django.forms import ValidationError
from django.forms import DateInput
from .mixins import ValidationMixin
from .models import Agent, Client, CustomUser, Feedback


class RegistrationForm(forms.ModelForm, ValidationMixin):
    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name','date_birth')
        widgets = {
            'date_birth': DateInput(attrs={'type': 'date'}),
        }
    

class UpdateForm(forms.ModelForm, ValidationMixin):
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'gender', 'profile_image')
 

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
        self.check_password_length(self.cleaned_data.get('password1'))
        self.check_age(self.cleaned_data.get('date_birth'))

    
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
        self.check_email(self.cleaned_data.get('email'))
        self.check_passwords(self.cleaned_data.get('password1'), self.cleaned_data.get('password2'))


class LoginForm(forms.Form):
    class Meta:
        model = CustomUser
        fields = ('email', 'password',)

    email = forms.CharField(max_length=255)
    password = forms.CharField(max_length=255, widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)


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
            })
        

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
            })
            

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        exclude = ('client',)

            
class BalanceForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ('balance',)
    
    def clean(self):
        if self.cleaned_data.get('balance') < 0:
            raise ValidationError("Balance must be > 0")
        else:
            return self.cleaned_data.get('balance')

