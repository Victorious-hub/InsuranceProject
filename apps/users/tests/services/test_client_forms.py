import pytest
from apps.users.services import client_register
from apps.users.forms import ClientRegistrationForm

@pytest.mark.django_db
def test_client_form_incorrect_password(client_service_incorrect_password_fixture):
    user = client_service_incorrect_password_fixture
    form = ClientRegistrationForm(data=user)
    assert not form.is_valid()

@pytest.mark.django_db
def test_client_form_email_exists(client_form_email_exists_fixture):
    user = client_form_email_exists_fixture
    client_register(user)
    form = ClientRegistrationForm(data=user)
    assert not form.is_valid()