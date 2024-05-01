
from apps.users.models import Feedback
from .models import Vacancy

def vacancy_list() -> Vacancy:
    obj = Vacancy.objects.all().values('title', 'description', 'created_at')
    return obj

def feedback_list() -> Vacancy:
    obj = Feedback.objects.all()
    return obj