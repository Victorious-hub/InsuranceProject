import pytest

@pytest.mark.django_db
def test_custom_user_model(custom_user_factory):
    user = custom_user_factory.create()
    assert user.email == "test@gmail.com"