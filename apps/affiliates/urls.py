from django.urls import path

from .views import ContractCreateView


urlpatterns = [
    path('contract/create/<int:pk>', ContractCreateView.as_view(), name='contract_create'),
] 