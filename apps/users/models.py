from datetime import datetime
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from PIL import Image
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.hashers import make_password

from .managers import UserManager

from django.core.validators import (
    MinValueValidator, 
    RegexValidator, 
    MaxValueValidator, 
    MinLengthValidator,
    MaxLengthValidator
)

class Affiliate(models.Model):
    name = models.CharField(max_length=255, blank=True)
    address = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=255, blank=True, validators=[RegexValidator(r"\+375 \((29|33|25)\) \d{3}-\d{2}-\d{2}"), MinLengthValidator(19), MaxLengthValidator(19)])

    class Meta:
        verbose_name = "affiliate"
        verbose_name_plural = "affiliates"

    def __str__(self):
        return f"Affiliate: {self.name}"

# здесь можете с нуля user не создавать кста. Есть AbstractUser просто
class CustomUser(AbstractBaseUser, PermissionsMixin): 
    date_birth = models.DateField(blank=True, null=True)
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    age = models.PositiveIntegerField(blank=True, null=True, validators=[MinValueValidator(18), MaxValueValidator(120)])
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_client = models.BooleanField(default=False)
    profile_image = models.ImageField(null=True, blank=True, upload_to="images/")
    gender = models.CharField(
        choices=(
                ("Male", "Male"),
                ("Female", "Female"),
            ), 
        blank=True, 
        null=True
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()

    def __str__(self):
        return f"Base User: {self.first_name} - {self.last_name}"
    
    def save(self, *args, **kwargs):
        if self.password and not self.password.startswith(('pbkdf2_sha256$', 'bcrypt$', 'argon2')):
            self.password = make_password(self.password)
        
        if self.date_birth:
            self.age = datetime.now().year - self.date_birth.year
        super().save(*args, **kwargs)
        if self.profile_image:
            img = Image.open(self.profile_image.path)
            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img.thumbnail(output_size)
                img.save(self.profile_image.path)
    

class Client(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    address = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=255, blank=True, 
                             validators=[
                                RegexValidator(r"\+375 \((29|33|25)\) \d{3}-\d{2}-\d{2}", 
                                message="Phone number must have format +375 (29) XXX-XX-XX "), 
                                MinLengthValidator(19), MaxLengthValidator(19)])
    balance = models.FloatField(default=0)

    class Meta:
        verbose_name = "client"
        verbose_name_plural = "clients"

    def __str__(self):
        return f"Client: {self.user.first_name} - {self.user.last_name}"


class Agent(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    affiliate = models.ForeignKey(Affiliate, on_delete=models.DO_NOTHING)
    salary = models.FloatField(default=0)
    tariff_rate = models.IntegerField(default=10)

    class Meta:
        verbose_name = "agent"
        verbose_name_plural = "agents"

    def __str__(self):
        return f"Agent: {self.user.first_name} - {self.user.last_name}"


class Feedback(models.Model):
    client = models.ForeignKey(Client, on_delete=models.DO_NOTHING)
    title = models.CharField(max_length=255)
    affiliate = models.ForeignKey(Affiliate, on_delete=models.DO_NOTHING)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    rating = models.IntegerField(default=5, validators=[MinValueValidator(1), MaxValueValidator(5)])

    class Meta:
        verbose_name = "feedback"
        verbose_name_plural = "feedbacks"

    def __str__(self):
        return f"Contract for client: {self.client.user.first_name}"
    