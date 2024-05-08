from collections import OrderedDict
from apps.users.constants import AGENT, CLIENT
import pytest
import factory

from apps.affiliates.tests.factories import AnswerFactory, CompanyFactory, ContractFactory, InsuranceObjectFactory, InsuranceRiskFactory, InsuranceTypeFactory, NewsFactory, PolicyFactory, PrivacyPolicyFactory, QuestionFactory, VacancyFactory
from pytest_factoryboy import register # type: ignore
from faker import Factory as FakerFactory # type: ignore

from apps.users.tests.factories import (
    CustomUserClientFactory, 
    CustomUserAgentFactory, 
    ClientFactory,
    AgentFactory,
    AffiliateFactory
)

faker = FakerFactory.create()

@pytest.fixture
def client_service_incorrect_password_fixture():
    user = OrderedDict(
        [
            ('email', "test1234@gmail.com"),
            ('first_name', factory.LazyFunction(lambda: faker.name())),
            ('last_name', "last_name"),
            ('role', CLIENT),
            ('password1', "12345678"),
            ('password2', "1234567"),
        ]
    )
    return user

@pytest.fixture
def client_form_email_exists_fixture():
    user = OrderedDict(
        [
            ('email', "test1234@gmail.com"),
            ('first_name', factory.LazyFunction(lambda: faker.name())),
            ('last_name', factory.LazyFunction(lambda: faker.name())),
            ('role', CLIENT),
            ('password1', "12345678"),
            ('password2', "12345678"),
        ]
    )
    return user

@pytest.fixture
def feedback_service_fixture(client_form_email_exists_fixture):
    user = OrderedDict(
        [
            ('client', client_form_email_exists_fixture),
            ('title', factory.LazyFunction(lambda: faker.name())),
            ('description', factory.LazyFunction(lambda: faker.name())),
            ('created_at', factory.LazyFunction(lambda: faker.date_time_this_year())),
            ('updated_at', factory.LazyFunction(lambda: faker.date_time_this_year())),
            ('rating', 3),
        ]
    )
    return user


@pytest.fixture
def client_service_data_check_fixture():
    user = OrderedDict(
        [
            ('email', "test_patient@gmail.com"),
            ('first_name', factory.LazyFunction(lambda: faker.name())),
            ('last_name', "last_name"),
            ('role', CLIENT),
            ('address', None),
            ('phone', None),
            ('balance', 0),
            ('password1', "12345678"),
            ('password2', "1234567"),
        ]
    )
    return user

register(CustomUserClientFactory)
register(CustomUserAgentFactory)
register(AffiliateFactory)
register(ClientFactory)
register(AgentFactory)

register(CompanyFactory)
register(VacancyFactory)
register(NewsFactory)
register(PrivacyPolicyFactory)
register(AnswerFactory)
register(QuestionFactory)

register(PolicyFactory)
register(ContractFactory)
register(InsuranceRiskFactory)
register(InsuranceObjectFactory)
register(InsuranceTypeFactory)
