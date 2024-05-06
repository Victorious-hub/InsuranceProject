import pytest
import io

from pytest_factoryboy import register
from faker import Factory as FakerFactory

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
