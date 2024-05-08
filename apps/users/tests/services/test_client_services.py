import pytest
from apps.users.services import balance_update, client_register, feedback_create
from django.contrib.auth import login, authenticate, logout

@pytest.mark.django_db
def test_client_creation(client_form_email_exists_fixture):
    user = client_form_email_exists_fixture
    client = client_register(user)
    assert client.user.email == user['email']
    assert len(client.user.password) > 7
    assert client

@pytest.mark.django_db
def test_feedback_creation(feedback_service_fixture):
    feedback = feedback_service_fixture
    client = client_register(feedback['client'])
    feedback_obj = feedback_create(client.user.id, feedback)
    assert client
    assert client.user.email == feedback['client']['email']
    assert feedback_obj

@pytest.mark.django_db
def test_login(client_form_email_exists_fixture):
    user_data = client_form_email_exists_fixture
    client = client_register(user_data)
    user_auth = authenticate(client, email=user_data['email'], password=user_data['password1'])
    assert user_auth.is_authenticated
