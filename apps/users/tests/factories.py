from apps.users.models import Affiliate, Agent, Client, CustomUser, Feedback
import factory
from faker import Factory as FakerFactory, Faker

faker = FakerFactory.create()

fake = Faker()

class CustomUserClientFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CustomUser
        
    first_name = factory.LazyFunction(lambda: faker.name())
    last_name = factory.LazyFunction(lambda: faker.name())
    email = "test@gmail.com"
    password = '1111111'
    gender = 'Male'
    role = 1 # Client

class CustomUserAgentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CustomUser
        
    first_name = factory.LazyFunction(lambda: faker.name())
    last_name = factory.LazyFunction(lambda: faker.name())
    email = "test_agent@gmail.com"
    password = '1111111'
    gender = 'Male'
    role = 2 # Agent

class ClientFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Client

    user = factory.SubFactory(CustomUserClientFactory)
    address = factory.LazyFunction(lambda: faker.name())
    phone = "+375 (29) 111-10-12"

class AffiliateFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Affiliate

    name = factory.LazyFunction(lambda: faker.name())
    address = factory.LazyFunction(lambda: faker.name())
    phone = factory.LazyFunction(lambda: faker.name())

class AgentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Agent

    user = factory.SubFactory(CustomUserAgentFactory)
    affiliate = factory.SubFactory(AffiliateFactory)
    salary = 0
    tariff_rate = 10

class FeedbackFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Feedback
    
    client = factory.SubFactory(CustomUserClientFactory)
    title = factory.LazyFunction(lambda: faker.name())
    description = factory.LazyFunction(lambda: faker.name())
    rating = 5


class FeedbackFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Feedback
    
    client = factory.SubFactory(CustomUserClientFactory)
    title = factory.LazyFunction(lambda: faker.name())
    description = factory.LazyFunction(lambda: faker.name())
    rating = 5