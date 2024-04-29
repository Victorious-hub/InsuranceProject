from django.urls import path

from .views import (
    AgentProfileView, 
    AuthenticateView, 
    ChangePasswordView, 
    ClientProfileView, 
    ClientRegistrationView, 
    LogoutView,
    UpdateAgentProfileView, 
    UpdateClientProfileView,
)

urlpatterns = [
    path('register/client/', ClientRegistrationView.as_view(), name='client_register'),
    path('register/agent/', ClientRegistrationView.as_view(), name='agent_register'),
    path('authenticate/', AuthenticateView.as_view(), name='authenticate'),
    path('client/<int:pk>', ClientProfileView.as_view(), name='client_profile'),
    path('agent/<int:pk>', AgentProfileView.as_view(), name='agent_profile'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('password/change/<int:pk>', ChangePasswordView.as_view(), name='change_password'),
    path('client/update/<int:pk>', UpdateClientProfileView.as_view(), name='client_update'),
    path('agent/update/<int:pk>', UpdateAgentProfileView.as_view(), name='agent_update'),
] 