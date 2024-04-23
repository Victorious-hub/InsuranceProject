from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import ClientRegisterForm

class ClientCreateView(CreateView):
    template_name = "client_register.html"
    form_class = ClientRegisterForm
    success_url = reverse_lazy("login")

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(self.success_url)
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        response = super().form_valid(form)
        user = form.save(commit=False)
        user.role = 'C'
        user.save()
        messages.success(self.request, "You have signed up successfully.")
        return response

    def form_invalid(self, form):
        messages.error(self.request, "Invalid submission.")
        return super().form_invalid(form)
