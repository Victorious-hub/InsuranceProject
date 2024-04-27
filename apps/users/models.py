from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.text import slugify

from .constants import GENDERS, ROLE_CHOICES
from django.contrib.auth.hashers import make_password
from .managers import UserManager

class Affiliate(models.Model):
    name = models.CharField(max_length=255, blank=True)
    address = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=255, blank=True)

    class Meta:
        verbose_name = "affiliate"
        verbose_name_plural = "affiliates"

    def __str__(self):
        return f"Affiliate: {self.name}"


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    gender = models.CharField(max_length=255, choices=GENDERS, blank=True, null=True)
    last_name = models.CharField(max_length=255)
    age = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()

    def __str__(self):
        return f"Base User: {self.first_name} - {self.last_name}"
    
    def save(self, *args, **kwargs):
        if self.password and not self.password.startswith(('pbkdf2_sha256$', 'bcrypt$', 'argon2')):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)
    

class Client(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    address = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=255, blank=True)

    class Meta:
        verbose_name = "client"
        verbose_name_plural = "clients"

    def __str__(self):
        return f"Client: {self.user.first_name} - {self.user.last_name}"


class Agent(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    affiliate = models.ForeignKey(Affiliate, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "agent"
        verbose_name_plural = "agents"

    def __str__(self):
        return f"Agent: {self.user.first_name} - {self.user.last_name}"
