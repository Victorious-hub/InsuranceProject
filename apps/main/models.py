from django.db import models
from django.utils import timezone

class BaseModel(models.Model):
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

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