from django.utils.translation import gettext_lazy as _

CREATED = 1
CONFIRMED = 2
COMPLETED = 3

CONTRACTS = (
    (CREATED, 'Created'),
    (CONFIRMED, 'Confirmed'),
    (COMPLETED, 'Completed'),
)

MEDICAL = 10
HOUSE = 20
CAR = 30

INSURANCE = (
    (MEDICAL, 'Medical Insuracne'),
    (HOUSE, 'House Insuracne'),
    (HOUSE, 'Car'),
)