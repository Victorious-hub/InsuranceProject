import pytest
from apps.users.models import Affiliate, Agent, Client, CustomUser

@pytest.mark.django_db
def test_compnay_creation(company_factory):
    company = company_factory.create()
    assert company

@pytest.mark.django_db
def test_question_creation(question_factory):
    question = question_factory.create()
    assert question

@pytest.mark.django_db
def test_answer_creation(answer_factory):
    answer = answer_factory.create()
    assert answer

@pytest.mark.django_db
def test_privacy_policy_creation(privacy_policy_factory):
    privacy_policy = privacy_policy_factory.create()
    assert privacy_policy

@pytest.mark.django_db
def test_news_creation(news_factory):
    company = news_factory.create()
    assert company

@pytest.mark.django_db
def test_vacancy_creation(vacancy_factory):
    vacancy = vacancy_factory.create()
    assert vacancy