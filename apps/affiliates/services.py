from apps.users.models import Affiliate, Agent, Client
from apps.users.utils import get_object

from .models import (
    Contract,
    Coupon, 
    InsuranceObject, 
    InsuranceRisk, 
    InsuranceType, 
    Policy
)
CREATED = 1
CONFIRMED = 3
COMPLETED = 4

def contract_create(pk: int, data) -> Contract:
    affiliate = get_object(Affiliate, id=data.get('affiliate'))
    insurance_type = get_object(InsuranceType, id=data.get('insurance_type'))
    insurance_object = get_object(InsuranceObject, id=data.get('insurance_object'))
    obj = Contract.objects.create(
        client=get_object(Client, user__id=pk),
        insurance_type=insurance_type,
        insurance_object=insurance_object,
        affiliate=affiliate,
        status=CREATED
    )

    for insurance_risks in data.get('insurance_risk'):
        risk = get_object(InsuranceRisk, id=insurance_risks)
        obj.insurance_risk.add(risk)
        obj.save()

    obj.full_clean()
    obj.save()
    return obj

def contract_update(pk: int, data):
  contract = Contract.objects.filter(client__user__id=pk).last()
  contract.affiliate = get_object(Affiliate, id=data.get('affiliate'))
  contract.insurance_type = get_object(InsuranceType , id=data.get('insurance_type'))
  contract.insurance_object = get_object(InsuranceObject, id=data.get('insurance_object'))
  contract.insurance_risk.set(data.get('insurance_risk'))  # Use set() for many-to-many
  contract.save()
  return contract


def policy_create(pk: int, data) -> Policy:
    agent: Agent = get_object(Agent, user__id=pk)
    contract: Contract = get_object(Contract, id=data.get('contract'))
    contract.status=CONFIRMED
    contract.save()
    obj = Policy.objects.create(
        agent=agent,
        contract=contract,
        insurance_sum=data.get('insurance_sum'),
        start_date=data.get('start_date'),
        end_date=data.get('end_date'),
        price=data.get('price')
    )

    agent.salary += contract.insurance_type.type/100 * float(obj.insurance_sum) * float(agent.tariff_rate)

    agent.save()
    obj.full_clean()
    obj.save()
    return obj

def apply_discount_if_coupon_exists(policy: Policy, code: str):
    coupon: Coupon = get_object(Coupon, code=code)
    price = policy.price
    client = policy.contract.client
    if coupon and coupon.active:
        price *= (coupon.discount / 100)
        if (policy.price - price) < client.balance:
            policy.price -= price
            coupon.active = False
            coupon.save()
            return True
        else:
            return False
    return True

def deduct_balance_and_complete_contract(policy: Policy):
    client = policy.contract.client
    if client.balance >= policy.price:
        client.balance -= policy.price
        policy.contract.status=COMPLETED
        client.save()
        policy.contract.save()
        policy.save()
        return True
    return False

def apply_coupon_and_pay(policy: Policy, code: str):
    if apply_discount_if_coupon_exists(policy, code):
        return deduct_balance_and_complete_contract(policy)
    else:
        return False