from django.utils.translation import gettext_lazy as _

CLIENT = 1
AGENT = 2

ROLE_CHOICES = (
    (CLIENT, 'Client'),
    (AGENT, 'Agent'),
)


GENDERS = (
    ('Male', _('Male')),
    ('Female', _('Female')),
)