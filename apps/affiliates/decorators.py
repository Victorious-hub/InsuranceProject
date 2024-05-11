from django.shortcuts import redirect
from functools import wraps

def client_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_client == True:
            return view_func(request, *args, **kwargs)
        return redirect('login')
    return _wrapped_view

def agent_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_staff == True:
            return view_func(request, *args, **kwargs)
        return redirect('login')
    return _wrapped_view

def superuser_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_superuser == True:
            return view_func(request, *args, **kwargs)
        return redirect('login')
    return _wrapped_view