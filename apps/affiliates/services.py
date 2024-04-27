from apps.users.models import Agent, Client
from apps.users.utils import get_object
from .models import Contract

def contract_create(pk: int, data) -> Contract:
    # 'client', 'insurance_type', 'insurance_sum', 'start_date', 'end_date'
    agent: Agent = get_object(Agent, user__id=pk)
    obj = Contract.objects.create(
        client=get_object(Client, id=data.get('client')),
        insurance_type=data.get('insurance_type'),
        insurance_sum=data.get('insurance_sum'),
        start_date=data.get('start_date'),
        end_date=data.get('end_date'),
        agent=agent,
        affiliate=agent.affiliate
    )

    obj.full_clean()
    obj.save()
    return obj