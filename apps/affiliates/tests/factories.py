from apps.affiliates.models import Company, BaseModel, Contacts, Contract, InsuranceObject, InsuranceRisk, News, Policy, Question, Answer, PrivacyPolicy, InsuranceType, Vacancy
from apps.users.models import Agent
from apps.users.tests.factories import AffiliateFactory, AgentFactory, ClientFactory
import factory
from faker import Factory as FakerFactory, Faker

faker = FakerFactory.create()

fake = Faker()

class CompanyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Company
        
    information = factory.LazyFunction(lambda: faker.name())

class QuestionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Question
    
    text = factory.LazyFunction(lambda: faker.name())

class AnswerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Answer
    
    text = factory.LazyFunction(lambda: faker.name()) 
    question = factory.SubFactory(QuestionFactory)

class PrivacyPolicyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PrivacyPolicy
    
    text = factory.LazyFunction(lambda: faker.name()) 

class NewsFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = News
    
    title = factory.LazyFunction(lambda: faker.name())
    content = factory.LazyFunction(lambda: faker.name())

class VacancyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Vacancy
    
    title = factory.LazyFunction(lambda: faker.name())
    description = factory.LazyFunction(lambda: faker.name())
    salary = factory.LazyFunction(lambda: faker.random_number())
    experience = factory.LazyFunction(lambda: faker.random_number())  


class InsuranceTypeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = InsuranceType

    type = factory.LazyFunction(lambda: faker.random_int(min=1, max=3))
    description = factory.LazyFunction(lambda: faker.text())


class InsuranceObjectFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = InsuranceObject

    name = factory.LazyFunction(lambda: faker.word())
    description = factory.LazyFunction(lambda: faker.text())


class InsuranceRiskFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = InsuranceRisk

    insurance_object = factory.SubFactory(InsuranceObjectFactory)
    name = factory.LazyFunction(lambda: faker.word())
    description = factory.LazyFunction(lambda: faker.text())


class ContractFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Contract

    client = factory.SubFactory(ClientFactory)  # Assuming you have ClientFactory
    affiliate = factory.SubFactory(AffiliateFactory)  # Assuming you have AffiliateFactory
    insurance_type = factory.SubFactory(InsuranceTypeFactory)
    insurance_object = factory.SubFactory(InsuranceObjectFactory)
    is_completed = factory.LazyFunction(lambda: faker.random_int(min=1, max=5))


class PolicyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Policy

    agent = factory.SubFactory(AgentFactory)  # Assuming you have AgentFactory
    contract = factory.SubFactory(ContractFactory)
    insurance_sum = factory.LazyFunction(lambda: faker.random_number())
    price = factory.LazyFunction(lambda: faker.random_number())
    start_date = factory.LazyFunction(lambda: faker.date_between(start_date='-30d', end_date='today'))
    end_date = factory.LazyFunction(lambda: faker.date_between(start_date='today', end_date='+30d'))
