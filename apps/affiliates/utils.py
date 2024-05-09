
import os
import requests
from django.conf import settings
import pandas as pd
import matplotlib.pyplot as plt
from apps.users.models import Client
from .constants import COMPLETED
from .models import Policy
from django.db.models import Sum
from statistics import median, mean, mode
from django.db.models import Q


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

def get_cat_info():
    response = requests.get('https://catfact.ninja/fact')
    return response.json()

def get_age(name: str):
    response = requests.get(f'https://api.agify.io/?name={name}')
    return response.json()


def plot_policy_sale():
    policies = Policy.objects.values('agent__affiliate')
    df = pd.DataFrame.from_records(policies)
    counts = df['agent__affiliate'].value_counts()
    counts.plot(kind='bar')

    plt.xlabel('Affiliate')
    plt.ylabel('Number of Policies')
    plt.title('Total Policies by Affiliate')
    plt.savefig(os.path.join(settings.MEDIA_ROOT, 'total_policies_by_affiliate.png'))

    plt.close()