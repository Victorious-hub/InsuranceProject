from django.db import models
from apps.users.models import Agent, Client, Affiliate
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

class BaseModel(models.Model):
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


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
    description = models.TextField()

    class Meta:
        verbose_name = "insurance"
        verbose_name_plural = "insurance"

    def __str__(self):
        return f"{self.type} insurance object"


class InsuranceObject(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    class Meta:
        verbose_name = "object"
        verbose_name_plural = "objects"

    def __str__(self):
        return f"{self.name} insurance object"


class InsuranceRisk(models.Model):
    insurance_object = models.ForeignKey(InsuranceObject, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()


    class Meta:
        verbose_name = "risk"
        verbose_name_plural = "risks"

    def __str__(self):
        return f"{self.name} risk"



class Contract(models.Model):
    class CompleteType(models.TextChoices):
        PAYED = 1, _('Payed')
        COMPLETED = 2, _('Completed')
        NOT_PAYED = 3, _('Not payed')
    

    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    affiliate = models.ForeignKey(Affiliate, on_delete=models.CASCADE)
    insurance_type = models.ForeignKey(InsuranceType, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    insurance_object = models.ForeignKey(InsuranceObject, on_delete=models.CASCADE)
    insurance_risk = models.ManyToManyField(InsuranceRisk)
    is_completed = models.CharField(max_length=20, choices=CompleteType.choices, default=CompleteType.NOT_PAYED)

    class Meta:
        verbose_name = "contract"
        verbose_name_plural = "contracts"

    def __str__(self):
        return f"Contract for client: {self.client.user.first_name}"


class Pollis(models.Model):
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE)
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE)
    insurance_sum = models.FloatField(default=0)
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField()

    def clean(self):
        if self.start_date > self.end_date:
            raise Exception("End date must be greater than start date")


class News(BaseModel):
    title = models.CharField(max_length=200)
    content = models.TextField()

    class Meta:
        verbose_name = "news"
        verbose_name_plural = "news"

    def __str__(self):
        return f"News: {self.title}"


class Vacancy(BaseModel):
    title = models.CharField(max_length=255)
    description = models.TextField()
    salary = models.IntegerField()
    experience = models.IntegerField()

    class Meta:
        verbose_name = "vacancy"
        verbose_name_plural = "vacancies"

    def __str__(self):
        return f"Vacancy: {self.title}"



    