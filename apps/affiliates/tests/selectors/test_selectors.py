import pytest
from apps.affiliates.selectors import (
    vacancy_list,
    incurance_list,
    get_client_contracts,
    get_client_contract,
    get_contracts,
    get_client_policy
)

@pytest.mark.django_db
def test_vacancy_list(vacancy_factory):
    vacancy_factory.create()
    obj = vacancy_list()
    assert obj is not None

@pytest.mark.django_db
def test_insurance_list(insurance_type_factory):
    insurance_type_factory.create()
    obj = incurance_list()
    assert obj is not None

@pytest.mark.django_db
def test_get_client_contracts(contract_factory, agent_factory):
    agent = agent_factory.create()
    contract_factory.create()
    obj = get_client_contracts(agent.user.id)
    assert obj is not None

@pytest.mark.django_db
def test_get_contracts(contract_factory):
    obj = contract_factory.create()
    client_contract = get_contracts(obj.client.user.id)
    assert client_contract is not None

# @pytest.mark.django_db
# def test_get_client_policy(policy_factory):
#     obj = policy_factory.create()
#     client_policy = get_client_policy(obj.contract.client.user.id)
#     assert client_policy is not None
