from apps.users.models import Agent, Client, CustomUser
import pytest

@pytest.mark.django_db
def test_custom_user_creation(custom_user_client_factory):
    user = custom_user_client_factory.create()
    assert user.email == "test@gmail.com"


@pytest.mark.django_db
def test_client_creation(client_factory):
    client: Client = client_factory.create()
    assert client.user.email == "test@gmail.com"
    assert isinstance(client, Client)
    assert client.user.is_staff is False
    assert client.user.role == 1


@pytest.mark.django_db
def test_agent_creation(agent_factory):
    agent: Agent = agent_factory.create()
    assert agent.user.email == "test_agent@gmail.com"
    assert isinstance(agent, Agent)
    assert agent.user.role == 2

@pytest.mark.django_db
def test_client_model_fields(client_factory):
    client: Client = client_factory.create()
    assert isinstance(client.user.first_name, str)
    assert isinstance(client.address, str)

@pytest.mark.django_db
def test_agent_model_fields(agent_factory):
    agent: Agent = agent_factory.create()
    assert isinstance(agent.affiliate.name, str)

@pytest.mark.django_db
def test_client_model_save(client_factory):
    client: Client = client_factory.create()
    client.user.first_name = 'New Name'
    client.save()
    assert client.user.first_name == 'New Name'

@pytest.mark.django_db
def test_agent_model_save(agent_factory):
    agent: Agent = agent_factory.create()
    agent.affiliate.name = 'New Agency'
    agent.save()
    assert agent.affiliate.name == 'New Agency'