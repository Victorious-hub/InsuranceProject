from django.shortcuts import render
from django.views.generic import TemplateView
from django.views import View
from .services import feedback_list, vacancy_list


class BaseView(TemplateView):
    template_name = 'main/base.html'


class VacnacyListView(TemplateView):
    template_name = 'main/vacancy.html'

    def get(self, request):
        vacancies = vacancy_list()
        return render(request, self.template_name, context={"vacancies": vacancies})


class FeedbackListView(View):
    template_name = 'main/feedback.html'

    def get(self, request):
        feedbacks = feedback_list()
        print(feedbacks.values())
        return render(request, self.template_name, context={"feedbacks": feedbacks})