import pytest
from apps.users.selectors import client_get, agent_get, policy_agent_list

@pytest.mark.django_db
def test_client_list(client_factory):
    client = client_factory.create()
    obj = client_get(client.user.id)
    assert obj

@pytest.mark.django_db
def test_client_retrieve(agent_factory):
    agent = agent_factory.create()
    obj = agent_get(agent.user.id)
    assert obj

@pytest.mark.django_db
def test_client_retrieve_check_fields(client_factory):
    client = client_factory.create()
    obj = client_get(client.user.id)
    assert obj.user.first_name == client.user.first_name
    assert obj.address == client.address
