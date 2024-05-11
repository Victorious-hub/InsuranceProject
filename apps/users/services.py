
from .utils import get_object
from .models import Affiliate, Agent, Client, CustomUser, Feedback
from django.contrib.auth.hashers import make_password
from datetime import datetime

def client_register(data) -> Client:
    user = CustomUser(
        first_name=data.get('first_name'),
        last_name=data.get('last_name'),
        email=data.get('email'),
        password = make_password(data.get('password1')),
        date_birth = datetime.strptime(data.get('date_birth'), "%Y-%m-%d"),
        is_client=True
    )
    user.save()
    client = Client(
        user=user,
    )
    client.full_clean()
    client.save()
    return client


def client_update(pk: int, data, profile_image) -> Client:
    client: Client = get_object(Client, user__id=pk)
    client.address = data.get('address')
    client.phone = data.get('phone')
    client.user.gender = data.get('gender')
    client.user.first_name = data.get('first_name')
    client.user.last_name = data.get('last_name')
    client.user.age = data.get('age')
    if profile_image:
        client.user.profile_image = profile_image

    client.user.save()
    client.save()
    return client

def agent_update(pk: int, data, profile_image) -> Agent:
    agent: Agent = get_object(Agent, user__id=pk)
    agent.user.gender = data.get('gender')
    agent.user.first_name = data.get('first_name')
    agent.user.last_name = data.get('last_name')
    if profile_image:
        agent.user.profile_image = profile_image
    
    agent.user.save()
    agent.save()
    return agent


def feedback_create(pk: int, data) -> Feedback:
    client = get_object(Client, user__id=pk)
    obj = Feedback.objects.create(
        client=client,
        title=data.get('title'),
        affiliate=get_object(Affiliate, id=data.get('affiliate')),
        description=data.get('description'),
        rating=data.get('rating')
    )
    obj.full_clean()
    obj.save()
    return obj

def balance_update(pk: int, balance: float) -> Client:
    client: Client = get_object(Client, user__id=pk)
    client.balance += float(balance)

    client.save()
    return client

