from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View
from apps.users.constants import AGENT, CLIENT
from .models import Contract, Pollis
from .services import contract_create, feedback_list, incurance_list, vacancy_list
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import ContractForm, PollisForm
from django.views.generic import TemplateView


class ContractCreateView(LoginRequiredMixin, View):
    template_name = 'contract_create.html'
    model = Contract
    form_class = ContractForm
    success_url = 'client_profile'

    def get(self, request, pk):
        if not self.request.user.is_authenticated or request.user.role != CLIENT:
            return redirect("login")
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


class BaseView(TemplateView):
    template_name = 'main/base.html'


class VacnacyListView(TemplateView):
    template_name = 'main/vacancy.html'

    def get(self, request):
        vacancies = vacancy_list()
        return render(request, self.template_name, context={"vacancies": vacancies})


class FeedbackListView(View):
    template_name = 'main/feedback.html'

    def get(self, request):
        feedbacks = feedback_list()
        return render(request, self.template_name, context={"feedbacks": feedbacks})


class InsuranceListView(View):
    template_name = 'main/insurance.html'

    def get(self, request):
        insurance = incurance_list()
        print(insurance)
        return render(request, self.template_name, context={"insurance": insurance})


class PollisCreateView(LoginRequiredMixin, View):
    template_name = 'pollis_create.html'
    model = Pollis
    form_class = PollisForm
    success_url = 'agent_profile'

    def get(self, request, pk):
        if not self.request.user.is_authenticated or request.user.role != AGENT:
            return redirect("login")
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