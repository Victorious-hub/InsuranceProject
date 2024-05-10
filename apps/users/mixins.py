from django.forms import ValidationError
from datetime import datetime
from .models import CustomUser


class ValidationMixin:

    def check_email(self, email: str) -> str:
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError("This email address is already registered.")
        return email
    
    def check_passwords(self, password1: str, password2: str) -> str:
        if password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2
    
    def check_age(self, date_birth: datetime) -> str:
        if date_birth is None:
            raise ValidationError("Birth date is null")
        elif datetime.now().year - date_birth.year < 18 or datetime.now().year - date_birth.year > 120:
            raise ValidationError("You must be 18+")
        else:
            return date_birth
    
    def check_password_length(self, password1) -> str:
        if len(password1) < 8:
            raise ValidationError("Password len must be at least 8 letters or numbers")
        return password1
    
    