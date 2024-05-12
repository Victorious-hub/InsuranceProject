from apps.users.models import Affiliate
import pytest
from apps.users.services import balance_update, client_register, feedback_create
from django.contrib.auth import login, authenticate, logout

@pytest.mark.django_db
def test_client_creation(client_fixture):
    user = client_fixture
    client = client_register(user)
    assert client.user.email == user['email']
    assert len(client.user.password) > 7
    assert client

# @pytest.mark.django_db
# def test_feedback_creation(feedback_fixture):
#     feedback = feedback_fixture
#     client = client_register(feedback['client'])
#     Affiliate.objects.create(
#         name = feedback_fixture.get()
#     )
#     feedback_obj = feedback_create(client.user.id, feedback)
#     assert client
#     assert feedback_obj

@pytest.mark.django_db
def test_login(client_fixture):
    user_data = client_fixture
    client = client_register(user_data)
    user_auth = authenticate(client, email=user_data['email'], password=user_data['password1'])
    assert user_auth.is_authenticated
