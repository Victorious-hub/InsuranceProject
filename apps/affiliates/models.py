from django.db import models
from django.forms import ValidationError
from .constants import INSURANCE_TYPE
from apps.users.models import Agent, Client, Affiliate

class Company(models.Model):
    information = models.TextField()

    class Meta:
        verbose_name = "company"
        verbose_name_plural = "Companies"

    def __str__(self):
        return f"Company: {self.name}"


class Contacts(models.Model):
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE)
    description =  models.TextField()

    class Meta:
        verbose_name = "company"
        verbose_name_plural = "Companies"

    def __str__(self):
        return f"Company: {self.name}"

class Question(models.Model):
    text = models.TextField()

    class Meta:
        verbose_name = "question"
        verbose_name_plural = "questions"

    def __str__(self):
        return f"Question: {self.text}"

class Answer(models.Model):
    text = models.TextField()
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "answer"
        verbose_name_plural = "answeries"

    def __str__(self):
        return f"Answer: {self.text}"

class PrivacyPolicy(models.Model):
    text = models.TextField()

    class Meta:
        verbose_name = "privacyPolicy"
        verbose_name_plural = "privacyPolicies"

    def __str__(self):
        return f"privacyPolicy"


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

    