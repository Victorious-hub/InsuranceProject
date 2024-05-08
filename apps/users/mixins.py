

from django.forms import ValidationError

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
    
    def check_age(self, age) -> str:
        if age < 18 or age > 120:
            raise ValidationError("You must be 18+")
        return age
    