import pytest
import io

from pytest_factoryboy import register
from faker import Factory as FakerFactory

from apps.users.tests.factories import (
    CustomUserFactory, 
    ClientFactory,
    AgentFactory
)

faker = FakerFactory.create()


register(CustomUserFactory)
register(ClientFactory)
register(AgentFactory)
