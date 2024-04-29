from .constants import AGENT, CLIENT
from .utils import get_object
from .models import Agent, Client, CustomUser
from django.contrib.auth.hashers import make_password


def client_register(data) -> Client:
    user = CustomUser(
        first_name=data.get('first_name'),
        last_name=data.get('last_name'),
        email=data.get('email'),
        password = make_password(data.get('password1')),
        gender=data.get('gender'),
        age=data.get('age'),
        role=CLIENT
    )
    user.save()
    client = Client(
        user=user,
    )
    client.full_clean()
    client.save()
    return client


def agent_register(data) -> Client:
    user = CustomUser(
        first_name=data.get('first_name'),
        last_name=data.get('last_name'),
        email=data.get('email'),
        is_staff = True,
        password = make_password(data.get('password1')),
        age=data.get('age'),
        role=AGENT
    )
    user.save()
    client = Agent(
        user=user,
    )
    client.full_clean()
    client.save()
    return client


def client_get(pk: int) -> Client:
    client = get_object(Client, user__id=pk)
    return client

def agent_get(pk: int) -> Client:
    agent = get_object(Agent, user__id=pk)
    return agent

def client_update(pk: int, data) -> Client:
    client: Client = get_object(Client, user__id=pk)
    client.address = data.get('address')
    client.phone = data.get('phone')
    client.user.gender = data.get('gender')
    client.user.first_name = data.get('first_name')
    client.user.last_name = data.get('last_name')
    client.user.age = data.get('age')
    client.user.profile_image = data.get('profile_image')

    client.user.save()
    client.save()
    return client

def agent_update(pk: int, data) -> Agent:
    agent: Agent = get_object(Agent, user__id=pk)
    agent.user.gender = data.get('gender')
    agent.user.first_name = data.get('first_name')
    agent.user.last_name = data.get('last_name')
    agent.user.age = data.get('age')

    agent.user.save()
    agent.save()
    return agent
