
from .models import Vacancy

def vacancy_list() -> Vacancy:
    obj = Vacancy.objects.all()
    return obj