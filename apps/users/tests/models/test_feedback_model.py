from apps.users.models import Affiliate, Agent, Client, CustomUser
import pytest

@pytest.mark.django_db
def test_affiliate_creation(affiliate_factory):
    affiliate = affiliate_factory.create()
    assert affiliate.name
    assert affiliate.address
    assert affiliate.phone

@pytest.mark.django_db
def test_affiliate_multiple_creation(affiliate_factory):
    count = 5
    affiliates: Affiliate = affiliate_factory.create_batch(count)
    assert len(affiliates) == count

@pytest.mark.django_db
def test_affiliate_model_save(affiliate_factory):
    affiliate: Affiliate = affiliate_factory.create()
    affiliate.name = 'New Name'
    affiliate.save()
    assert affiliate.name == 'New Name'