from django.db import models
from apps.users.models import Agent, Client, Affiliate
from django.utils.translation import gettext_lazy as _
from django.contrib.postgres.fields import ArrayField

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


class InsuranceType(models.Model):
    class Insurance(models.TextChoices):
        MEDICAL = 'Medical', _('Medical Insuracne')
        HOUSE = 'House', _('House Insuracne')
    type = models.CharField(max_length=20, choices=Insurance.choices)
    insurance_sum = models.FloatField()
    risks = ArrayField(models.CharField(max_length=512))


class Contract(models.Model):
    class CompleteType(models.TextChoices):
        PAYED = 1, _('Payed')
        COMPLETED = 2, _('Completed')
        NOT_PAYED = 3, _('Not payed')

    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    affiliate = models.ForeignKey(Affiliate, on_delete=models.CASCADE)
    insurance_type = models.ForeignKey(InsuranceType, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_completed = models.CharField(max_length=20, choices=CompleteType.choices)

    class Meta:
        verbose_name = "contract"
        verbose_name_plural = "contracts"

    def __str__(self):
        return f"Contract for client: {self.client.user.first_name}"


    