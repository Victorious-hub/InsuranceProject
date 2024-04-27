from django.shortcuts import redirect, render
from django.urls import reverse_lazy, reverse
from django.views import View
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.mixins import LoginRequiredMixin

from .constants import AGENT, CLIENT
from .services import agent_get, agent_update, client_get, client_register, client_update

from .models import Agent, Client, CustomUser
from .forms import AgentUpdateForm, ClientRegistrationForm, ClientUpdateForm, LoginForm


class ClientRegistrationView(View):
    template_name = 'auth/client_register.html'
    model = Client
    form_class = ClientRegistrationForm
    success_url = reverse_lazy('authenticate')

    def get(self, request):
        if self.request.user.is_authenticated:
            if request.user.role == CLIENT:
                client_profile_url = reverse("client_profile", kwargs={'pk': request.user.id})
                return redirect(client_profile_url)
            elif request.user.role == AGENT:
                agent_profile_url = reverse("agent_profile", kwargs={'pk': request.user.id})
                return redirect(agent_profile_url)
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            client_register(form.data)
            return redirect(self.success_url)
        else:
            for _, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{error}")
        return render(request, self.template_name, {'form': form})


# class AgentRegistrationView(View):
#     template_name = 'auth/agent_register.html'
#     model = Agent
#     form_class = AgentRegistrationForm
#     success_url = reverse_lazy('authenticate')

#     def get(self, request):
#         if self.request.user.is_authenticated:
#             if request.user.role == CLIENT:
#                 client_profile_url = reverse("client_profile", kwargs={'pk': request.user.id})
#                 return redirect(client_profile_url)
#             elif request.user.role == AGENT:
#                 agent_profile_url = reverse("agent_profile", kwargs={'pk': request.user.id})
#                 return redirect(agent_profile_url)
#         form = self.form_class()
#         return render(request, self.template_name, {'form': form})

#     def post(self, request):
#         form = self.form_class(request.POST)
#         if form.is_valid():
#             client_register(form.data)
#             return redirect(self.success_url)  
#         return render(request, self.template_name, {'form': form})


class AuthenticateView(View):
    template_name = "auth/authenticate.html"
    form_class = LoginForm
    client_success_url = "client_profile"
    agent_success_url = "agent_profile"

    def get(self, request):
        if self.request.user.is_authenticated:
            if request.user.role == CLIENT:
                client_profile_url = reverse("client_profile", kwargs={'pk': request.user.id})
                return redirect(client_profile_url)
            elif request.user.role == AGENT:
                agent_profile_url = reverse("agent_profile", kwargs={'pk': request.user.id})
                return redirect(agent_profile_url)
        form = self.form_class()
        return render(request, self.template_name, context={"form": form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = authenticate(
                request,
                email=form.cleaned_data["email"],
                password=form.cleaned_data["password"]
            )

            if user:
                login(request, user)
                if request.user.role == CLIENT:
                    client_profile_url = reverse(self.client_success_url, kwargs={'pk': request.user.id})
                    return redirect(client_profile_url)
                elif request.user.role == AGENT:
                    agent_profile_url = reverse(self.agent_success_url, kwargs={'pk': request.user.id})
                    return redirect(agent_profile_url)
        else:
            for _, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{error}")
        return render(request, self.template_name, {"form": form})


class ClientProfileView(View, LoginRequiredMixin):
    template_name = "clients/client_profile.html"
    success_url = reverse_lazy("main")
    
    def get(self, request, pk):
        if not self.request.user.is_authenticated or request.user.role != CLIENT:
            return redirect("authenticate")
        client = client_get(pk)
        return render(request, self.template_name, context={"client": client})


class AgentProfileView(View, LoginRequiredMixin):
    template_name = "agents/agent_profile.html"
    
    def get(self, request, pk):
        if not self.request.user.is_authenticated or request.user.role != AGENT:
            return redirect("authenticate")
        agent = agent_get(pk)
        return render(request, self.template_name, context={"agent": agent})


class LogoutView(View):
    success_url = reverse_lazy('authenticate')

    def get(self, request):
        logout(request)
        return redirect(self.success_url)
    

class ChangePasswordView(LoginRequiredMixin, View):
    model = CustomUser
    template_name = "auth/change_password.html"
    form_class = PasswordChangeForm
    success_url = reverse_lazy("authenticate")

    def get(self, request, pk):
        if not self.request.user.is_authenticated:
            return redirect("authenticate")
        form = self.form_class(request.user)
        return render(request, self.template_name, context={'form': form})
    

    def post(self, request, pk):
        form = self.form_class(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Your password was successfully updated!")
            return redirect(self.success_url)
        else:
            messages.error(request, "Please correct the error below.")
        return render(request, self.template_name, {"form": form})


class UpdateClientProfileView(LoginRequiredMixin, View):
    model = Client
    form_class = ClientUpdateForm
    template_name = "clients/client_data.html"
    success_url = "client_profile"

    def get(self, request, pk):
        if not self.request.user.is_authenticated or request.user.role != CLIENT:
            return redirect("authenticate")
        client = client_get(pk)  
        form = self.form_class(instance=client, user=request.user)
        return render(request, self.template_name, context={"form": form})

    def post(self, request, pk):
        form = self.form_class(request.POST)
        if form.is_valid():
            client = client_update(pk, form.data)
            if client:
                client_profile_url = reverse(self.success_url, kwargs={'pk': request.user.id})
                return redirect(client_profile_url)
        return render(request, self.template_name, {"form": form})


class UpdateAgentProfileView(LoginRequiredMixin, View):
    model = Agent
    form_class = AgentUpdateForm
    template_name = "agents/agent_data.html"
    success_url = "agent_profile"

    def get(self, request, pk):
        if not self.request.user.is_authenticated or request.user.role != CLIENT:
            return redirect("authenticate")
        client = client_get(pk)  
        form = self.form_class(instance=client, user=request.user)
        return render(request, self.template_name, context={"form": form})

    def post(self, request, pk):
        form = self.form_class(request.POST)
        if form.is_valid():
            client = agent_update(pk, form.data)
            if client:
                client_profile_url = reverse(self.success_url, kwargs={'pk': request.user.id})
                return redirect(client_profile_url)
        return render(request, self.template_name, {"form": form})