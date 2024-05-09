import logging
from django.shortcuts import redirect, render
from django.urls import reverse_lazy, reverse
from django.views import View
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout

from .constants import CLIENT, AGENT

from .decorators import agent_required, client_required
from django.utils.decorators import method_decorator
from .models import Agent, Client, CustomUser, Feedback

from .forms import (
    AgentUpdateForm, 
    BalanceForm, 
    ClientRegistrationForm, 
    ClientUpdateForm, 
    FeedbackForm, 
    LoginForm
)

from .services import (
    agent_update, 
    balance_update, 
    client_register, 
    client_update, 
    feedback_create
)

from .selectors import agent_get, policy_agent_list, client_get

user_logger = logging.getLogger('main')

class ClientRegistrationView(View):
    template_name = 'auth/client_register.html'
    model = Client
    form_class = ClientRegistrationForm
    success_url = reverse_lazy('login')

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            client_register(form.data)
            user_logger.info(f"Register user: {form.data.get('first_name')}-{form.data.get('last_name')}")
            return redirect(self.success_url)
        else:
            for _, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{error}")
        return render(request, self.template_name, {'form': form})

class AuthenticateView(View):
    template_name = 'auth/authenticate.html'
    form_class = LoginForm
    success_url = 'main'

    def get(self, request):
        if self.request.user.is_authenticated:
            return redirect(self.success_url)
        form = self.form_class()
        return render(request, self.template_name, context={'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = authenticate(
                request,
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password']
            )

            if user:
                login(request, user)
                user_logger.info(f"Register user: {self.request.user}")
                return redirect(self.success_url)
        else:
            user_logger.error(f"Failed to login user: {form.data.get('first_name')}-{form.data.get('last_name')}")
            for _, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{error}')
                    
        return render(request, self.template_name, {'form': form})


@method_decorator(client_required, name='dispatch')
class ClientProfileView(View):
    # permission_required = 'users.change_client'
    template_name = 'clients/client_profile.html'
    
    def get(self, request, pk):
        client = client_get(pk)
        user_logger.info(f"Client data: {client.user.first_name}-{client.user.last_name}")
        return render(request, self.template_name, context={'client': client})
    

@method_decorator(agent_required, name='dispatch')
class AgentProfileView(View):
    template_name = 'agents/agent_profile.html'
    
    def get(self, request, pk):
        agent = agent_get(pk)
        user_logger.info(f"Client data: {agent.user.first_name}-{agent.user.last_name}")
        return render(request, self.template_name, context={'agent': agent})


class LogoutView(View):
    success_url = reverse_lazy('login')

    def get(self, request):
        logout(request)
        user_logger.error(f"Logout user: {request.user}")
        return redirect(self.success_url)
    

class ChangePasswordView(View):
    model = CustomUser
    template_name = 'auth/change_password.html'
    form_class = PasswordChangeForm
    success_url = reverse_lazy('login')

    def get(self, request, pk):
        if not self.request.user.is_authenticated:
            return redirect(self.success_url)
        form = self.form_class(request.user)
        return render(request, self.template_name, context={'form': form})
    

    def post(self, request, pk):
        form = self.form_class(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            user_logger.info(f"Successfully changed password for user: {request.user}")
            return redirect(self.success_url)
        else:
            user_logger.error(f"Error to change password: {request.user}")
            messages.error(request, 'Please correct the error below.')
        return render(request, self.template_name, {'form': form})


@method_decorator(client_required, name='dispatch')
class UpdateClientProfileView(View):
    model = Client
    form_class = ClientUpdateForm
    template_name = 'clients/client_data.html'
    success_url = 'client_profile'

    def get(self, request, pk):
        client = client_get(pk)  
        form = self.form_class(instance=client, user=request.user)
        return render(request, self.template_name, context={'form': form})

    def post(self, request, pk):
        form = self.form_class(request.POST)
        if form.is_valid():
            client = client_update(pk, form.data,  request.FILES.get('profile_image'))
            if client:
                user_logger.info(f"Updated data for client: {request.user}")
                client_profile_url = reverse(self.success_url, kwargs={'pk': request.user.id})
                return redirect(client_profile_url)
        return render(request, self.template_name, {'form': form})


@method_decorator(agent_required, name='dispatch')
class UpdateAgentProfileView(View):
    model = Agent
    form_class = AgentUpdateForm
    template_name = 'agents/agent_data.html'
    success_url = 'agent_profile'

    def get(self, request, pk):
        client = client_get(pk)  
        form = self.form_class(instance=client, user=request.user)
        return render(request, self.template_name, context={'form': form})

    def post(self, request, pk):
        form = self.form_class(request.POST)
        if form.is_valid():
            agent = agent_update(pk, form.data, request.FILES.get('profile_image'))
            if agent:
                user_logger.info(f"Updated data for agent: {request.user}")
                agent_profile_url = reverse(self.success_url, kwargs={'pk': request.user.id})
                return redirect(agent_profile_url)
        return render(request, self.template_name, {'form': form})


@method_decorator(agent_required, name='dispatch')
class ContractAgentListView(View):
    model = Agent
    template_name = 'agents/agent_contracts.html'
    success_url = 'agent_profile'

    def get(self, request, pk):
        contracts = policy_agent_list(pk)  
        return render(request, self.template_name, context={'contracts': contracts})


@method_decorator(client_required, name='dispatch')
class FeedbackCreateView(View):
    model = Feedback
    form_class = FeedbackForm
    template_name = 'clients/feedback_create.html'
    success_url = 'client_profile'

    def get(self, request, pk):
        form = self.form_class()
        return render(request, self.template_name, context={'form': form})
    
    def post(self, request, pk):
        form = self.form_class(request.POST)
        if form.is_valid():
            feedback = feedback_create(pk, form.data)
            if feedback:
                # user_logger.info(f"Client feedback: {request.user}")
                client_profile_url = reverse(self.success_url, kwargs={'pk': request.user.id})
                return redirect(client_profile_url)
        return render(request, self.template_name, {'form': form})
    

@method_decorator(client_required, name='dispatch')
class FillBalanceView(View):
    model = Client
    form_class = BalanceForm
    template_name = 'clients/balance_create.html'
    success_url = 'client_profile'

    def get(self, request, pk):
        form = self.form_class()
        return render(request, self.template_name, context={'form': form})
    
    def post(self, request, pk):
        form = self.form_class(request.POST)
        if form.is_valid():
            balance = balance_update(pk, form.data)
            if balance:
                # user_logger.info(f"Client balance has been updated successfully: {request.user}")
                client_profile_url = reverse(self.success_url, kwargs={'pk': request.user.id})
                return redirect(client_profile_url)
        return render(request, self.template_name, {'form': form})