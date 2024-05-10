from apps.users.models import Affiliate, Agent, Client, Feedback
from apps.users.utils import get_object
from .constants import CREATED
from .models import Contract, InsuranceType, News, Policy, Vacancy
from django.db.models import Q

def vacancy_list() -> Vacancy:
    obj = Vacancy.objects.all().values('title', 'description', 'created_at')
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
        Q(is_completed=CREATED)).order_by('client__user__email')
    return contracts

def get_contracts(pk: int) -> Contract:
    client = get_object(Client, user__id = pk)
    contracts = Contract.objects.filter(client=client)
    return contracts

def get_client_contract(pk: int) -> Contract:
    contract = get_object(Contract, id=pk)
    return contract

def get_client_policy(pk: int) -> Policy:
    policy = Policy.objects.filter(contract__id=pk).first()
    return policy