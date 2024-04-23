from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.text import slugify
from .constants import GENDERS, ROLES
from .managers import UserManager
from django.db.models import F

class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = None
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    address = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    role = models.CharField(max_length=255, choices=ROLES, blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()

    def __str__(self):
        return f"Base User: {self.first_name} - {self.last_name}"

class Client(CustomUser):
    gender = models.CharField(max_length=255, choices=GENDERS, blank=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True, editable=False)

    class Meta:
        verbose_name = "client"
        verbose_name_plural = "clients"

    def __str__(self):
        return f"Client: {self.first_name} - {self.last_name}"

    def save(self, *args, **kwargs):
        slug_data = self.email.split('@')[0]
        self.slug = slugify(slug_data)
        return super(Client, self).save(*args, **kwargs)


class Agent(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=255, unique=True, blank=True, editable=False)

    class Meta:
        verbose_name = "agent"
        verbose_name_plural = "agents"

    def __str__(self):
        return f"Agent: {self.user.first_name} - {self.user.last_name}"

    def save(self, *args, **kwargs):
        slug_data = self.user.email.split('@')[0]
        self.slug = slugify(slug_data)
        return super(Agent, self).save(*args, **kwargs)