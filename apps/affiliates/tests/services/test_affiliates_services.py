from datetime import datetime
import pytest
from apps.affiliates.services import ( 
    contract_create, 
    policy_create, 
    apply_discount_if_coupon_exists, 
    deduct_balance_and_complete_contract, 
    apply_coupon_and_pay
)

@pytest.mark.django_db
def test_contract_create(
                    affiliate_factory, 
                    insurance_type_factory, 
                    insurance_object_factory, 
                    client_factory, 
                    insurance_risk_factory
                ):
    affiliate = affiliate_factory.create()
    insurance_type = insurance_type_factory.create()
    insurance_object = insurance_object_factory.create()
    client = client_factory.create()
    insurance_risk = insurance_risk_factory.create()
    data = {
        'affiliate': affiliate.id,
        'insurance_type': insurance_type.id,
        'insurance_object': insurance_object.id,
        'insurance_risk': [insurance_risk.id],
    }
    contract = contract_create(client.user.id, data)
    assert contract is not None
    assert contract.client == client
    assert contract.insurance_type == insurance_type
    assert contract.insurance_object == insurance_object
    assert contract.affiliate == affiliate
    assert contract.insurance_risk.first() == insurance_risk

@pytest.mark.django_db
def test_policy_create(agent_factory, contract_factory):
    agent = agent_factory.create()
    contract = contract_factory.create()
    data = {
        'contract': contract.id,
        'insurance_sum': 1000,
        'start_date': '2022-01-01',
        'end_date': '2023-01-01',
        'price': 100,
    }
    policy = policy_create(agent.user.id, data)
    assert policy is not None
    assert policy.agent == agent
    assert policy.contract == contract
    assert policy.insurance_sum == data['insurance_sum']
    assert policy.start_date == datetime.strptime(data['start_date'], '%Y-%m-%d').date()
    assert policy.end_date == datetime.strptime(data['end_date'], '%Y-%m-%d').date()
    assert policy.price == data['price']

@pytest.mark.django_db
def test_apply_discount_if_coupon_exists(policy_factory, coupon_factory):
    policy = policy_factory.create(price=100)
    coupon = coupon_factory.create(code='TEST', discount=10, active=True)
    apply_discount_if_coupon_exists(policy, coupon.code)
    assert policy.price == 10.


@pytest.mark.django_db
def test_deduct_balance_and_complete_contract(client_factory, policy_factory):
    client = client_factory.create(balance=100)
    policy = policy_factory.create(price=50, contract__client=client)
    assert deduct_balance_and_complete_contract(policy)
    assert client.balance == 50
    assert policy.contract.is_completed

@pytest.mark.django_db
def test_apply_coupon_and_pay(client_factory, policy_factory, coupon_factory):
    client = client_factory.create(balance=100)
    policy = policy_factory.create(price=50, contract__client=client)
    coupon = coupon_factory.create(code='TEST', discount=10, active=True)
    assert apply_coupon_and_pay(policy, coupon.code)
    assert policy.price == 5.
    assert client.balance == 95.
    assert policy.contract.is_completed
