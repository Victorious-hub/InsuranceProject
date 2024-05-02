from django.urls import path

from .views import (
    AgentProfileView, 
    AuthenticateView, 
    ChangePasswordView, 
    ClientProfileView, 
    ClientRegistrationView,
    ContractAgentListView,
    FeedbackCreateView,
    FillBalanceView, 
    LogoutView,
    UpdateAgentProfileView, 
    UpdateClientProfileView,
)

urlpatterns = [
    path('register/client/', ClientRegistrationView.as_view(), name='client_register'),
    path('register/agent/', ClientRegistrationView.as_view(), name='agent_register'),
    path('authenticate/', AuthenticateView.as_view(), name='login'),
    path('client/<int:pk>', ClientProfileView.as_view(), name='client_profile'),
    path('agent/<int:pk>', AgentProfileView.as_view(), name='agent_profile'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('password/change/<int:pk>', ChangePasswordView.as_view(), name='change_password'),
    path('client/update/<int:pk>', UpdateClientProfileView.as_view(), name='client_update'),
    path('agent/update/<int:pk>', UpdateAgentProfileView.as_view(), name='agent_update'),
    path('agent/contracts/<int:pk>', ContractAgentListView.as_view(), name='agent_contracts'),
    path('client/feedbacks/create/<int:pk>', FeedbackCreateView.as_view(), name='feedback_create'),
    path('client/balance/create/<int:pk>', FillBalanceView.as_view(), name='balance_create')
] 