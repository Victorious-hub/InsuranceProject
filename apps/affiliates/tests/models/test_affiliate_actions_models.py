import pytest

@pytest.mark.django_db
def test_insurance_type_creation(insurance_type_factory):
    insurance_type = insurance_type_factory.create()
    assert insurance_type

@pytest.mark.django_db
def test_insurance_object_creation(insurance_object_factory):
    insurance_object = insurance_object_factory.create()
    assert insurance_object

@pytest.mark.django_db
def test_insurance_risk_creation(insurance_risk_factory):
    insurance_risk = insurance_risk_factory.create()
    assert insurance_risk

@pytest.mark.django_db
def test_contract_creation(contract_factory):
    contract = contract_factory.create()
    assert contract

@pytest.mark.django_db
def test_policy_creation(policy_factory):
    policy = policy_factory.create()
    assert policy