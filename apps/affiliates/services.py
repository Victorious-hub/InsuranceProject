from apps.users.models import Affiliate, Agent, Client, Feedback
from apps.users.utils import get_object
from .models import Contract, InsuranceObject, InsuranceRisk, InsuranceType, Pollis, Vacancy

def contract_create(pk: int, data) -> Contract:
    affiliate = get_object(Affiliate, id=data.get('affiliate'))
    insurance_type = get_object(InsuranceType, id=data.get('insurance_type'))
    insurance_object = get_object(InsuranceObject, id=data.get('insurance_object'))
    obj = Contract.objects.create(
        client=get_object(Client, user__id=pk),
        insurance_type=insurance_type,
        insurance_object=insurance_object,
        affiliate=affiliate
    )

    for insurance_risks in data.get('insurance_risk'):
        risk = get_object(InsuranceRisk, id=insurance_risks)
        obj.insurance_risk.add(risk)
        obj.save()

    obj.full_clean()
    obj.save()
    return obj


def pollis_create(pk: int, data) -> Pollis:
    agent: Agent = get_object(Agent, user__id=pk)
    contract: Contract = get_object(Contract, id=data.get('contract'))
    contract.is_completed = Contract.CompleteType.COMPLETED
    obj = Pollis.objects.create(
        agent=agent,
        contract=contract,
        insurance_sum=data.get('insurance_sum'),
        start_date=data.get('start_date'),
        end_date=data.get('end_date'),
    )

    obj.full_clean()
    obj.save()
    return obj

def vacancy_list() -> Vacancy:
    obj = Vacancy.objects.all().values('title', 'description', 'created_at')
    return obj

def feedback_list() -> Vacancy:
    obj = Feedback.objects.all()
    return obj

def incurance_list() -> InsuranceType:
    obj = InsuranceType.objects.all()
    return obj