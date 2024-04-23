from django.db import models
from django.forms import ValidationError

from .constants import INSURANCE_TYPE
from apps.users.models import Agent, Client


class Affiliate(models.Model):
    name = models.CharField(max_length=255, blank=True)
    address = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=255, blank=True)
    agents = models.ManyToManyField(Agent)

    class Meta:
        verbose_name = "affiliate"
        verbose_name_plural = "affiliates"

    def __str__(self):
        return f"Affiliate: {self.name}"


class Contract(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE)
    affility = models.ForeignKey(Affiliate, on_delete=models.CASCADE)
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