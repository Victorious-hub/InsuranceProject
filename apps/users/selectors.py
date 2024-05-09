from apps.affiliates.models import Contract, Client, Agent, Policy
from .utils import get_object


def policy_agent_list(id: int) -> Contract:
    agent = get_object(Agent, user__id=id)

    obj = Policy.objects.filter(agent=agent)
    return obj

def client_get(pk: int) -> Client:
    client = get_object(Client, user__id=pk)
    return client

def agent_get(pk: int) -> Client:
    agent = get_object(Agent, user__id=pk)
    return agent
