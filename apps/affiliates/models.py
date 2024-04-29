from django.db import models
from django.forms import ValidationError
from django.utils import timezone
from .constants import INSURANCE_TYPE
from apps.users.models import Agent, Client, Affiliate

class BaseModel(models.Model):
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Company(BaseModel):
    name = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    affiliates = models.ManyToManyField(Affiliate)

    class Meta:
        verbose_name = "company"
        verbose_name_plural = "Companies"

    def __str__(self):
        return f"Company: {self.name}"


class Contract(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE)
    affiliate = models.ForeignKey(Affiliate, on_delete=models.CASCADE)
    insurance_type = models.CharField(max_length=255, choices=INSURANCE_TYPE, blank=True)
    insurance_sum = models.FloatField()
    start_date  = models.DateField()
    end_date = models.DateField()

    class Meta:
        verbose_name = "affiliate"
        verbose_name_plural = "affiliates"

    def __str__(self):
        return f"Contract for client: {self.client.user.first_name}"
    
    def clean(self):
        if self.start_date >= self.end_date:
            raise ValidationError("End date cannot be before start date")

    