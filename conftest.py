from apps.affiliates.tests.factories import AnswerFactory, CompanyFactory, NewsFactory, PrivacyPolicyFactory, QuestionFactory, VacancyFactory
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


