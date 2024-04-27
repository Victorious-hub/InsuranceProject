

from django.forms import ValidationError

from .utils import get_object
from .models import CustomUser


class ValidationMixin:

    def _clean_email(self, email: str) -> str:
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError("This email address is already registered.")
        return email
    
    def _clean_passwords(self, password1: str, password2: str) -> str:
        if password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2