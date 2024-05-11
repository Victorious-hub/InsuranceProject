from apps.users.models import Affiliate, Agent, Feedback
from apps.users.utils import get_object
from .models import Contract, InsuranceType, News, Policy, Vacancy
from django.db.models import Q
CREATED = 1
SIGNED = 2
CONFIRMED = 3
COMPLETED = 4

def vacancy_list() -> Vacancy:
    obj = Vacancy.objects.all()
    return obj

def feedback_list() -> Feedback:
    obj = Feedback.objects.all()
    return obj

def affiliate_list() -> Affiliate:
    obj = Affiliate.objects.all()
    return obj

def news_list() -> News:
    obj = News.objects.all()
    return obj

def incurance_list() -> InsuranceType:
    obj = InsuranceType.objects.all()
    return obj

def get_client_contracts(pk: int) -> Contract:
    agent: Agent = get_object(Agent, user__id=pk)
    contracts: Contract = Contract.objects.filter(
        Q(affiliate=agent.affiliate) & 
        Q(status=SIGNED)).order_by('client__user__email')
    return contracts

def get_contracts(pk: int) -> Contract:
    contracts = Contract.objects.filter(client__user__id=pk)
    return contracts

def get_client_contract(pk: int) -> Contract:
    contract = get_object(Contract, id=pk)
    return contract

def get_client_policy(pk: int) -> Policy:
    policy = Policy.objects.filter(contract__id=pk).first()
    return policy