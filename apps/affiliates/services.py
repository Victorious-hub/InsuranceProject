from apps.users.models import Affiliate, Agent, Client
from apps.users.utils import get_object
from .constants import CONFIRMED, CREATED
from .models import (
    Contract, 
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
    )

    obj.full_clean()
    obj.save()
    return obj
