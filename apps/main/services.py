
from .models import Vacancy

def vacancy_list() -> Vacancy:
    obj = Vacancy.objects.all().values('title', 'description', 'created_at')
    return obj