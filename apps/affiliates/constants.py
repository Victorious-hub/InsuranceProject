from django.utils.translation import gettext_lazy as _

CREATED = 1
SIGNED = 2
CONFIRMED = 3
COMPLETED = 4

CONTRACTS = (
    (CREATED, 'Created'),
    (SIGNED, 'Signed'),
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