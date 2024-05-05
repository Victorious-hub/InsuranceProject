import logging
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View

from .constants import COMPLETED
from .decorators import agent_required, client_required
from .models import Contract, Policy
from .forms import ContractForm, PolicyForm
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from django.contrib import messages

from .selectors import (
    feedback_list,
    get_client_contract,
    get_client_contracts,
    get_client_policy,
    get_contracts, 
    incurance_list, 
    vacancy_list
)

from .services import apply_coupon_and_pay, contract_create, policy_create

affiliate_logger = logging.getLogger('affiliates')

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
                affiliate_logger.info(f"Created contract for client: {form.data.get('client')}")
                client_profile_url = reverse(self.success_url, kwargs={'pk': pk})
                return redirect(client_profile_url)
        return render(request, self.template_name, {'form': form})


class BaseView(TemplateView):
    affiliate_logger.info(f"Main page")
    template_name = 'main/base.html'


class VacnacyListView(TemplateView):
    template_name = 'main/vacancy.html'

    def get(self, request):
        vacancies = vacancy_list()
        affiliate_logger.info(f"Vacancy list page")
        return render(request, self.template_name, context={'vacancies': vacancies})


class FeedbackListView(View):
    template_name = 'main/feedback.html'

    def get(self, request):
        feedbacks = feedback_list()
        affiliate_logger.info(f"Feedback list page")
        return render(request, self.template_name, context={'feedbacks': feedbacks})


class InsuranceListView(View):
    template_name = 'main/insurance.html'

    def get(self, request):
        insurance = incurance_list()
        affiliate_logger.info(f"Insurance list page")
        return render(request, self.template_name, context={"insurance": insurance})


@method_decorator(agent_required, name='dispatch')
class PolicyCreateView(View):
    template_name = 'agent_actions/policy_create.html'
    model = Policy
    form_class = PolicyForm
    success_url = 'agent_profile'

    def get(self, request, pk):
        contract = get_client_contract(pk)
        form = self.form_class(initial={'contract': contract})
        return render(request, self.template_name, {'form': form})

    def post(self, request, pk):
        form = self.form_class(request.POST)
        if form.is_valid():
            policy = policy_create(pk, form.data)
            if policy:
                affiliate_logger.info(f"Policy for client: {request.user}")
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
        affiliate_logger.info(f"Client contract list: {request.user}")
        return render(request, self.template_name, {'contracts': contracts})

@method_decorator(client_required, name='dispatch')
class ConfirmPolicyCreateView(View):
    template_name = 'client_actions/policy_confirm.html'
    success_url = 'client_profile'

    def get(self, request, pk):
        policy = get_client_policy(pk)
        return render(request, self.template_name, {'policy': policy})

    def post(self, request, pk):
        coupon_code = request.POST.get('coupon')
        policy = get_client_policy(pk)
        success = apply_coupon_and_pay(policy, coupon_code)
        if success:
            affiliate_logger.info(f"Policy successfully confirmed: {request.user}")
            return redirect(reverse('main'))
        else:
            affiliate_logger.info(f"Error to confirm policy: {request.user}")
            messages.error(request, "Coupon is not valid!")
            return render(request, self.template_name, {'policy': policy})
        