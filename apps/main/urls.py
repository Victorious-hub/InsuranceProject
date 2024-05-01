from django.urls import  path
from .views import BaseView, FeedbackListView, VacnacyListView

urlpatterns = [
    path('', BaseView.as_view(), name='main'),
    path('vacancies/', VacnacyListView.as_view(), name='vacancy_list'),
    path('feedbacks/', FeedbackListView.as_view(), name='feedback_list'),
] 