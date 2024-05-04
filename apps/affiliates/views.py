from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View
from .decorators import agent_required, client_required
from .models import Contract, Policy
from .forms import ContractForm, PolicyForm
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator

from django.core.paginator import Paginator

from .selectors import (
    feedback_list,
    get_client_contracts,
    get_contracts, 
    incurance_list, 
    vacancy_list
)

from .services import contract_create, policy_create

@method_decorator(client_required, name='dispatch')
class ContractCreateView(View):
    template_name = 'client_actions/contract_create.html'
    model = Contract
    form_class = ContractForm
    success_url = 'client_profile'

    def get(self, request, pk):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, pk):
        form = self.form_class(request.POST)
        if form.is_valid():
            contract = contract_create(pk, form.data)
            if contract:
                client_profile_url = reverse(self.success_url, kwargs={'pk': pk})
                return redirect(client_profile_url)
        return render(request, self.template_name, {'form': form})


class BaseView(TemplateView):
    template_name = 'main/base.html'


class VacnacyListView(TemplateView):
    template_name = 'main/vacancy.html'

    def get(self, request):
        vacancies = vacancy_list()
        return render(request, self.template_name, context={'vacancies': vacancies})


class FeedbackListView(View):
    template_name = 'main/feedback.html'

    def get(self, request):
        feedbacks = feedback_list()
        return render(request, self.template_name, context={'feedbacks': feedbacks})


class InsuranceListView(View):
    template_name = 'main/insurance.html'

    def get(self, request):
        insurance = incurance_list()
        print(insurance)
        return render(request, self.template_name, context={"insurance": insurance})


@method_decorator(agent_required, name='dispatch')
class PolicyCreateView(View):
    template_name = 'agent_actions/policy_create.html'
    model = Policy
    form_class = PolicyForm
    success_url = 'agent_profile'

    def get(self, request, pk):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, pk):
        form = self.form_class(request.POST)
        print(form)
        if form.is_valid():
            policy = policy_create(pk, form.data)
            if policy:
                agent_profile_url = reverse(self.success_url, kwargs={'pk': pk})
                return redirect(agent_profile_url)
        return render(request, self.template_name, {'form': form})


@method_decorator(agent_required, name='dispatch')
class AgentContractsListView(View):
    template_name = 'agent_actions/affiliate_contracts.html'
    model = Contract
    form_class = ContractForm
    success_url = 'agent_profile'

    def get(self, request, pk):
        contracts = get_client_contracts(pk)
        return render(request, self.template_name, {'contracts': contracts})


@method_decorator(client_required, name='dispatch')
class ClientContractListView(View):
    template_name = 'client_actions/client_contracts.html'
    model = Contract
    form_class = ContractForm
    success_url = 'client_profile'

    def get(self, request, pk):
        contracts = get_contracts(pk)
        return render(request, self.template_name, {'contracts': contracts})
    