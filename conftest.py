from collections import OrderedDict
from datetime import datetime
import pytest
import factory

from apps.affiliates.tests.factories import AnswerFactory, CompanyFactory, ContractFactory, CouponFactory, InsuranceObjectFactory, InsuranceRiskFactory, InsuranceTypeFactory, NewsFactory, PolicyFactory, PrivacyPolicyFactory, QuestionFactory, VacancyFactory
from pytest_factoryboy import register # type: ignore
from faker import Factory as FakerFactory # type: ignore
CLIENT = 1
AGENT = 2

from apps.users.tests.factories import (
    CustomUserClientFactory, 
    CustomUserAgentFactory, 
    ClientFactory,
    AgentFactory,
    AffiliateFactory
)
faker = FakerFactory.create()

@pytest.fixture
def client_fixture():
    user = OrderedDict(
        [
            ('email', "test1234@gmail.com"),
            ('first_name', factory.LazyFunction(lambda: faker.name())),
            ('last_name', factory.LazyFunction(lambda: faker.name())),
            ('is_client', True),
            ('password1', "12345678"),
            ('password2', "12345678"),
            ('date_birth', '2004-10-10'),
            ('phone', "+375 (29) 111-10-12"),
            ('balanace', 100),
        ]
    )
    return user

@pytest.fixture
def affiliate_fixture():
    affiliate = OrderedDict(
        [
            ('id', 1),
            ('name', factory.LazyFunction(lambda: faker.name())),
            ('address', factory.LazyFunction(lambda: faker.name())),
            ('phone', "+375 (29) 111-10-12"),
        ]
    )
    return affiliate

@pytest.fixture
def feedback_fixture(client_fixture, affiliate_fixture):
    feedback = OrderedDict(
        [
            ('client', client_fixture),
            ('affiliate', affiliate_fixture),
            ('title', factory.LazyFunction(lambda: faker.name())),
            ('description', factory.LazyFunction(lambda: faker.name())),
            ('created_at', factory.LazyFunction(lambda: faker.date_time_this_year())),
            ('updated_at', factory.LazyFunction(lambda: faker.date_time_this_year())),
            ('rating', 3),
        ]
    )
    return feedback


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
register(CouponFactory)
