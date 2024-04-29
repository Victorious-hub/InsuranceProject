from django.shortcuts import render
from django.views.generic import TemplateView

from .services import vacancy_list

class MainView(TemplateView):
    template_name = 'main/main.html'


class VacnacyListView(TemplateView):
    template_name = 'main/vacancy.html'

    def get(self, request):
        vacancies = vacancy_list()
        print(vacancies)
        return render(request, self.template_name, context={"vacancies": vacancies})
