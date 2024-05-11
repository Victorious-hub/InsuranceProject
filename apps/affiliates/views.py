import logging
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View

from .decorators import agent_required, client_required, superuser_required
from .models import Answer, Company, Contract, Coupon, News
from .forms import ContractForm, PolicyForm
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.db.models import Q

from .selectors import (
    affiliate_list,
    feedback_list,
    get_client_contract,
    get_client_contracts,
    get_client_policy,
    get_contracts, 
    incurance_list, 
    vacancy_list
)

from .utils import (
    client_age_mean, 
    client_age_median, 
    client_age_mode, 
    client_list, 
    get_age, 
    get_cat_info, 
    plot_policy_sale, 
    policy_comleted_list_price, 
    policy_month_sale
)


from .services import (
    apply_coupon_and_pay, 
    contract_create, 
    policy_create
)

affiliate_logger = logging.getLogger('affiliates')

@method_decorator(client_required, name='dispatch')
class ContractCreateView(View):
    template_name = 'client_actions/contract_create.html'
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


@method_decorator(client_required, name='dispatch')
class ClientPolicyDetail(View):
    template_name = 'client_actions/policy_detail.html'

    def get(self, request, pk):
        policy = get_client_policy(pk)
        affiliate_logger.info(f"Client policy detail")
        return render(request, self.template_name, context={'policy': policy})


class BaseView(TemplateView):
    affiliate_logger.info(f"Main page")
    template_name = 'main/base.html'


class CompanyDetailView(View):
    template_name = 'main/company.html'

    def get(self, request):
        company = Company.objects.all()
        affiliate_logger.info(f"Company page")
        return render(request, self.template_name, context={'company': company})

class CouponListView(View):
    template_name = 'main/coupons.html'

    def get(self, request):
        coupon = Coupon.objects.filter(active=True)
        affiliate_logger.info(f"Coupon page")
        return render(request, self.template_name, context={'coupon': coupon})


class QuestionAnswerListView(View):
    template_name = 'main/question_answer.html'

    def get(self, request):
        answer = Answer.objects.all()
        affiliate_logger.info(f"Answer page")
        return render(request, self.template_name, context={'answer': answer})


class NewsListView(View):
    template_name = 'main/news.html'

    def get(self, request):
        news = News.objects.all()
        affiliate_logger.info(f"News page")
        return render(request, self.template_name, context={'news': news})


class VacnacyListView(View):
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

class AffiliateListView(View):
    template_name = 'main/affiliate_info.html'

    def get(self, request):
        affiliate = affiliate_list()
        affiliate_logger.info(f"Affiliate list page")
        return render(request, self.template_name, context={"affiliate": affiliate})


@method_decorator(agent_required, name='dispatch')
class PolicyCreateView(View):
    template_name = 'agent_actions/policy_create.html'
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
        else:
            for _, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{error}")
        return render(request, self.template_name, {'form': form})


@method_decorator(agent_required, name='dispatch')
class AgentContractsListView(View):
    template_name = 'agent_actions/affiliate_contracts.html'
    form_class = ContractForm
    success_url = 'agent_profile'

    def get(self, request, pk):
        contracts = get_client_contracts(pk)
        return render(request, self.template_name, {'contracts': contracts})
    

@method_decorator(client_required, name='dispatch')
class DeleteClientContractView(View):
    template_name = 'client_actions/delete_contract.html'
    success_url = 'client_contracts'

    def get(self, request, pk):
        contract = get_client_contract(pk)
        return render(request, self.template_name, {'contract': contract})

    def post(self, request, pk):
        contract = get_client_contract(pk)
        contract.delete()
        client_contracts = reverse(self.success_url, kwargs={'pk': pk})
        return redirect(client_contracts)

@method_decorator(client_required, name='dispatch')
class ContractSignView(View):
    template_name = 'client_actions/contract_sign.html'
    success_url = 'client_contracts'

    def get(self, request, pk):
        contract = get_client_contract(pk)
        return render(request, self.template_name, {'contract': contract})

    def post(self, request, pk):
        contract = get_client_contract(pk)
        if contract:
            contract.status = 2
            contract.save()
            affiliate_logger.info(f"Signed contract for client: {request.user}")
            client_profile_url = reverse(self.success_url, kwargs={'pk': pk})
            return redirect(client_profile_url)
        return render(request, self.template_name)
    
    
@method_decorator(agent_required, name='dispatch')
class SearchContractsView(View):
    model = Contract
    template_search_name = "agent_actions/affiliate_contracts_searched.html"
    template_name = 'agent_actions/affiliate_contracts.html'

    def post(self, request, pk):
        searched = request.POST["searched"]
        if len(searched) != 0:
            contracts = self.model.objects.filter(
                Q(client__user__email__contains=searched) | 
                Q(client__user__first_name__contains=searched) | 
                Q(client__user__last_name__contains=searched),
            )
            return render(request, self.template_search_name, {"searched": searched, "contracts": contracts})
        else:
            return render(request, self.template_name, {})



@method_decorator(client_required, name='dispatch')
class ClientContractListView(View):
    template_name = 'client_actions/client_contracts.html'
    form_class = ContractForm
    success_url = 'client_profile'

    def get(self, request, pk):
        contracts = get_contracts(pk)
        try:
            affiliate_logger.info(f"Client contract list: {request.user}")
            return render(request, self.template_name, {'contracts': contracts})
        except Exception:
           return render(request, self.template_name)


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
            messages.error(request, "Coupon is not valid or not enough balance!")
            return render(request, self.template_name, {'policy': policy})

@method_decorator(superuser_required, name='dispatch')
class StatisticsView(View):
    template_name = "statistics/base_statistics.html"

    def get(self, request, pk):
        return render(request, self.template_name)


@method_decorator(superuser_required, name='dispatch')
class CompanyStatisticsView(View):
    template_name = "statistics/company_statistics.html"

    def get(self, request, pk):
        total_clients = client_list()
        total_policy_price = policy_comleted_list_price()
        client_median = client_age_median()
        client_mean = client_age_mean()
        client_mode = client_age_mode()
        # plot_policy_sale()
        # policy_month_sale()
        return render(
            request, 
            self.template_name, 
            {
                'total_clients': total_clients,
                'total_policy_price': total_policy_price['price__sum'],
                'client_median': client_median,
                'client_mean': client_mean,
                'client_mode': client_mode
            })

@method_decorator(superuser_required, name='dispatch')
class CompanyPolicyChartDetailView(View):
    template_name = "statistics/policy_sale_statistics.html"

    def get(self, request, pk):
        policy_sale_image = plot_policy_sale()
        return render(request, self.template_name, {'policy_sale_image': policy_sale_image})

# @method_decorator(superuser_required, name='dispatch')
# class CompanyPolicyMonthChartDetailView(View):
#     template_name = "statistics/policy_sale_statistics.html"

#     def get(self, request, pk):
#         policy_month_image = policy_month_sale()
#         return render(request, self.template_name, {'policy_month_image': policy_month_image})
        

class CatFactView(View):
    template_name = 'main/cat_fact.html'

    def get(self, request):
        cat_fact = get_cat_info()
        return render(request, self.template_name, context={'cat_fact': cat_fact})

class AgePredictionView(View):
    template_name = 'main/age_prediction.html'

    def get(self, request):
        first_name = self.request.user.first_name
        age = get_age(first_name)
        return render(request, self.template_name, context={'age': age})
