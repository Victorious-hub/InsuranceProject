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
    affiliates = affiliate_factory.create_batch(count)
    assert len(affiliates) == count

@pytest.mark.django_db
def test_affiliate_model_save(affiliate_factory):
    affiliate: Affiliate = affiliate_factory.create()
    affiliate.name = 'New Name'
    affiliate.save()
    assert affiliate.name == 'New Name'

@pytest.mark.django_db
def test_affiliate_model_fields(affiliate_factory):
    affiliate: Affiliate = affiliate_factory.create()
    assert isinstance(affiliate.name, str)
    assert isinstance(affiliate.address, str)
    assert isinstance(affiliate.phone, str)

@pytest.mark.django_db
def test_affiliate_model_delete(affiliate_factory):
    affiliate: Affiliate = affiliate_factory.create()
    affiliate.delete()
    assert Affiliate.objects.filter(id=affiliate.id).count() == 0

@pytest.mark.django_db
def test_affiliate_model_update(affiliate_factory):
    affiliate: Affiliate = affiliate_factory.create()
    affiliate.phone = 'New Phone'
    affiliate.save()
    assert affiliate.phone == 'New Phone'
