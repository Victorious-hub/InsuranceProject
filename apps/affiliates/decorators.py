from django.shortcuts import redirect
from functools import wraps

from apps.users.constants import AGENT, CLIENT

def client_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.role != CLIENT:
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def agent_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.role != AGENT:
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return _wrapped_view