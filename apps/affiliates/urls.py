from django.urls import path

from .views import BaseView, ContractCreateView, FeedbackListView, InsuranceListView, PollisCreateView, VacnacyListView


urlpatterns = [
    path('pollis/create/<int:pk>', PollisCreateView.as_view(), name='contract_create'),          
    path('contract/create/<int:pk>', ContractCreateView.as_view(), name='contract_create'),
    path('', BaseView.as_view(), name='main'),
    path('vacancies/', VacnacyListView.as_view(), name='vacancy_list'),
    path('feedbacks/', FeedbackListView.as_view(), name='feedback_list'),
    path('insurance/', InsuranceListView.as_view(), name='insurance_list'),
] 