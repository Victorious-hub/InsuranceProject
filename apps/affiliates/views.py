from django.shortcuts import redirect, render
from django.urls import reverse_lazy, reverse
from django.views import View
from apps.users.constants import AGENT
from apps.affiliates.services import contract_create
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import ContractForm
from .models import Contract


class ContractCreateView(LoginRequiredMixin, View):
    template_name = 'contract_create.html'
    model = Contract
    form_class = ContractForm
    success_url = 'agent_profile'

    def get(self, request, pk):
        if not self.request.user.is_authenticated or request.user.role != AGENT:
            return redirect("authenticate")
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, pk):
        form = self.form_class(request.POST)
        if form.is_valid():
            contract = contract_create(pk, form.data)
            if contract:
                client_profile_url = reverse(self.success_url, kwargs={'pk': pk})
                return redirect(client_profile_url)
        return render(request, self.template_name, {"form": form})

