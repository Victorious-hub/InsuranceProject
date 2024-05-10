from apps.users.models import Affiliate, Agent, Client
from apps.users.utils import get_object
from .constants import (
    CAR, 
    COMPLETED, 
    CONFIRMED, 
    CREATED, 
    HOUSE, 
    MEDICAL
)

from .models import (
    Contract,
    Coupon, 
    InsuranceObject, 
    InsuranceRisk, 
    InsuranceType, 
    Policy
)

def contract_create(pk: int, data) -> Contract:
    affiliate = get_object(Affiliate, id=data.get('affiliate'))
    insurance_type = get_object(InsuranceType, id=data.get('insurance_type'))
    insurance_object = get_object(InsuranceObject, id=data.get('insurance_object'))
    obj = Contract.objects.create(
        client=get_object(Client, user__id=pk),
        insurance_type=insurance_type,
        insurance_object=insurance_object,
        affiliate=affiliate,
        is_completed=CREATED
    )

    for insurance_risks in data.get('insurance_risk'):
        risk = get_object(InsuranceRisk, id=insurance_risks)
        obj.insurance_risk.add(risk)
        obj.save()

    obj.full_clean()
    obj.save()
    return obj


def policy_create(pk: int, data) -> Policy:
    agent: Agent = get_object(Agent, user__id=pk)
    contract: Contract = get_object(Contract, id=data.get('contract'))
    contract.is_completed = CONFIRMED
    contract.save()
    obj = Policy.objects.create(
        agent=agent,
        contract=contract,
        insurance_sum=data.get('insurance_sum'),
        start_date=data.get('start_date'),
        end_date=data.get('end_date'),
        price=data.get('price')
    )

    match contract.insurance_type.type:
        case 1:
            agent.salary += (MEDICAL/100) * (float(obj.insurance_sum) * float(agent.tariff_rate/100))
        case 2:
            agent.salary += (HOUSE/100) * (float(obj.insurance_sum) * float(agent.tariff_rate/100))
        case 3:
            agent.salary += (CAR/100) * (float(obj.insurance_sum) * float(agent.tariff_rate/100))

    agent.save()
    obj.full_clean()
    obj.save()
    return obj

def apply_discount_if_coupon_exists(policy: Policy, code: str):
    if code:
        coupon: Coupon = get_object(Coupon, code=code)
        if coupon and coupon.active:
            policy.price *= (coupon.discount / 100)
            coupon.active = False
            coupon.save()

def deduct_balance_and_complete_contract(policy: Policy):
    client = policy.contract.client
    if client.balance >= policy.price:
        client.balance -= policy.price
        policy.contract.is_completed = COMPLETED
        client.save()
        policy.contract.save()
        policy.save()
        return True
    return False

def apply_coupon_and_pay(policy: Policy, code: str):
    apply_discount_if_coupon_exists(policy, code)
    return deduct_balance_and_complete_contract(policy)
