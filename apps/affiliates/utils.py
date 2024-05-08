
from apps.users.models import Client
from .constants import COMPLETED
from .models import Policy
from django.db.models import Sum
from statistics import median, mean, mode
from django.db.models import Q
import requests

def client_list()->Client:
    obj = Client.objects.all().order_by('user__first_name')
    return obj

def policy_comleted_list_price()->Policy:
    obj = Policy.objects.filter(contract__is_completed=COMPLETED).aggregate(Sum('price'))
    return obj

def client_age_median():
    obj = Client.objects.filter(~Q(user__age=None))
    return median(obj.values_list('user__age', flat=True))


def client_age_mode():
    obj = Client.objects.filter(~Q(user__age=None))
    return mean(obj.values_list('user__age', flat=True))


def client_age_mean():
    obj = Client.objects.filter(~Q(user__age=None))
    return mode(obj.values_list('user__age', flat=True))


