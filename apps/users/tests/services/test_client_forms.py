import collections
import pytest
from datetime import datetime
from apps.users.services import client_register
from apps.users.forms import BalanceForm, ClientRegistrationForm

@pytest.mark.django_db
def test_client_form_incorrect_password(client_fixture):
    user = client_fixture
    user['password2'] = '1234567'
    form = ClientRegistrationForm(data=user)
    assert not form.is_valid()

@pytest.mark.django_db
def test_client_form_incorrect_age(client_fixture):
    user = client_fixture
    user['date_birth'] = '2024-10-10'
    form = ClientRegistrationForm(data=user)
    assert not form.is_valid()

@pytest.mark.django_db
def test_client_form_length_password(client_fixture):
    user = client_fixture
    user['password2'] = '1234567'
    user['password1'] = '1234567'
    form = ClientRegistrationForm(data=user)
    assert not form.is_valid()

@pytest.mark.django_db
def test_client_form_email_exists(client_fixture):
    user = client_fixture
    client_register(user)
    form = ClientRegistrationForm(data=user)
    assert not form.is_valid()

@pytest.mark.django_db
def test_client_form_balanace_incorrect(client_fixture):
    user = client_fixture
    client = client_register(user)
    client.balance = -100
    client_data = collections.OrderedDict((field.name, getattr(client, field.name)) for field in client._meta.fields)
    form = BalanceForm(data=client_data)
    assert not form.is_valid()
