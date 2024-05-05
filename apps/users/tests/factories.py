from apps.users.models import Agent, Client, CustomUser
import factory
from faker import Factory as FakerFactory, Faker

faker = FakerFactory.create()

fake = Faker()

class CustomUserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CustomUser
        
    first_name = factory.LazyFunction(lambda: faker.name())
    last_name = factory.LazyFunction(lambda: faker.name())
    email = "test@gmail.com"
    password = '1111111'
    gender = 'M'
    role = 'C'

class ClientFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Client

    user = factory.SubFactory(CustomUserFactory)
    name = factory.Faker('name')
    address = factory.Faker('address')

class AgentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Agent

    # Assuming Agent model has these fields
    user = factory.SubFactory(CustomUserFactory)
    agency_name = factory.Faker('company')