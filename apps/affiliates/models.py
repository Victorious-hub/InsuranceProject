from django.db import models
from apps.users.models import Agent, Client, Affiliate
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator


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
        return f"Company: {self.information[:10]}"


class Contacts(models.Model):
    agent = models.ForeignKey(Agent, on_delete=models.DO_NOTHING)
    description =  models.TextField()

    class Meta:
        verbose_name = "company"
        verbose_name_plural = "Companies"

    def __str__(self):
        return f"Company: {self.description[:10]}"

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
        verbose_name_plural = "answers"

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
    type = models.PositiveSmallIntegerField(max_length=20, choices=(
        (10, 'Medical Insuracne'),
        (20, 'House Insuracne'),
        (30, 'Car'),
    ))
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
    
    client = models.ForeignKey(Client, on_delete=models.DO_NOTHING)
    affiliate = models.ForeignKey(Affiliate, on_delete=models.DO_NOTHING)
    insurance_type = models.ForeignKey(InsuranceType, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    insurance_object = models.ForeignKey(InsuranceObject, on_delete=models.DO_NOTHING)
    insurance_risk = models.ManyToManyField(InsuranceRisk)
    status = models.PositiveSmallIntegerField(max_length=20, choices=(
        (1, 'Created'),
        (2, 'Signed'),
        (3, 'Confirmed'),
        (4, 'Completed'),
    ))


    class Meta:
        verbose_name = "contract"
        verbose_name_plural = "contracts"

    def __str__(self):
        return f"Contract for client: {self.client.user.first_name}"


class Policy(BaseModel):
    agent = models.ForeignKey(Agent, on_delete=models.DO_NOTHING)
    contract = models.ForeignKey(Contract, on_delete=models.DO_NOTHING)
    insurance_sum = models.FloatField(default=0)
    price = models.FloatField(default=0)
    start_date = models.DateField()
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


class Coupon(BaseModel):
    code = models.CharField(max_length=255, unique=True)
    discount = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(100)])
    active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "coupon"
        verbose_name_plural = "coupons"

    def __str__(self):
        return f"Coupon: {self.code}"

    