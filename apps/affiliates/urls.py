from django.urls import path

from .views import (
    AffiliateListView,
    AgentContractsListView,
    BaseView,
    ClientContractListView,
    ClientPolicyDetail,
    ConfirmPolicyCreateView, 
    ContractCreateView, 
    FeedbackListView, 
    InsuranceListView,
    NewsListView,
    PolicyCreateView,
    SearchContractsView,
    StatisticsView, 
    VacnacyListView,
    AgePredictionView,
    CatFactView
)


urlpatterns = [
    path('client/contracts/policy/<int:pk>', ConfirmPolicyCreateView.as_view(), name='client_policy'),
    path('client/contracts/<int:pk>', ClientContractListView.as_view(), name='client_contracts'),
    path('policy/create/<int:pk>', PolicyCreateView.as_view(), name='policy_create'),          
    path('contract/create/<int:pk>', ContractCreateView.as_view(), name='contract_create'),
    path('', BaseView.as_view(), name='main'),
    path('vacancies/', VacnacyListView.as_view(), name='vacancy_list'),
    path('affiliate/', AffiliateListView.as_view(), name='affiliate_list'),
    path('news/', NewsListView.as_view(), name='news_list'),
    path('feedbacks/', FeedbackListView.as_view(), name='feedback_list'),
    path('insurance/', InsuranceListView.as_view(), name='insurance_list'),
    path('agent/client/contracts/<int:pk>', AgentContractsListView.as_view(), name='client_contract_list'),
    path('admin/statisctics/<int:pk>', StatisticsView.as_view(), name='stat'),
    path('client/policy/detail/<int:pk>', ClientPolicyDetail.as_view(), name='client_policy_detail'),
    path('cat/fact', CatFactView.as_view(), name='cat_fact'),
    path('age/prediction', AgePredictionView.as_view(), name='age_predict'),
    path('contract/search/<int:pk>', SearchContractsView.as_view(), name='search_contracts'),

] 