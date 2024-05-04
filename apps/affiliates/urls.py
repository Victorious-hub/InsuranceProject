from django.urls import path

from .views import (
    AgentContractsListView,
    BaseView,
    ClientContractListView, 
    ContractCreateView, 
    FeedbackListView, 
    InsuranceListView,
    PolicyCreateView, 
    VacnacyListView
)


urlpatterns = [
    path('client/contracts/<int:pk>', ClientContractListView.as_view(), name='client_contracts'),
    path('policy/create/<int:pk>', PolicyCreateView.as_view(), name='policy_create'),          
    path('contract/create/<int:pk>', ContractCreateView.as_view(), name='contract_create'),
    path('', BaseView.as_view(), name='main'),
    path('vacancies/', VacnacyListView.as_view(), name='vacancy_list'),
    path('feedbacks/', FeedbackListView.as_view(), name='feedback_list'),
    path('insurance/', InsuranceListView.as_view(), name='insurance_list'),
    path('agent/client/contracts/<int:pk>', AgentContractsListView.as_view(), name='client_contract_list'),
] 