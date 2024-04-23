from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from .views import ClientCreateView

urlpatterns = [
    path('register/', ClientCreateView.as_view(), name='client_register'),
] 