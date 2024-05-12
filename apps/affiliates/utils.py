
import base64
import io
import os
from urllib import parse
import requests
from django.conf import settings
import pandas as pd
import matplotlib.pyplot as plt
from django.db.models import Count
from apps.users.models import Affiliate, Client
from apps.users.utils import get_object
from .models import Policy
from django.db.models import Sum
from statistics import median, mean, mode
from django.db.models import Q
from datetime import datetime
import matplotlib.pyplot as plt

def client_list()->Client:
    obj = Client.objects.all().order_by('user__first_name')
    return obj

def policy_comleted_list_price()->Policy:
    obj = Policy.objects.filter(contract__status=4).aggregate(Sum('price'))
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
  confirmed_policies = Policy.objects.filter(contract__status=4)
  policy_counts = confirmed_policies.values('agent__affiliate').annotate(count=Count('id'))

  affiliates = [pc['agent__affiliate'] for pc in policy_counts]
  counts = [pc['count'] for pc in policy_counts]

  plt.bar([get_object(Affiliate, id=affiliate).name for affiliate in affiliates], counts)
  plt.xticks(rotation=30, ha='right')  

  bar_label([get_object(Affiliate, id=affiliate).name for affiliate in affiliates], counts)

  plt.xlabel('Affiliate Name')
  plt.ylabel('Policy Count')
  plt.title(f"Confirmed Policies by Affiliates")

  fig = plt.gcf()
  buf = io.BytesIO()
  fig.savefig(buf, format='png')
  buf.seek(0)
  string = base64.b64encode(buf.read())
  url = parse.quote(string)
  return url

def bar_label(x, y):
  for i, value in enumerate(y):
    plt.text(x[i], value + 0.1, str(value), ha='center') 




def policy_month_sale():
    today = datetime.now()
    policies = Policy.objects.all()

    month_counts = {month: 0 for month in range(1, 13)}

    for policy in policies:
        created_month = policy.created_at.month
        if created_month <= today.month:
            month_counts[created_month] += 1

    month_labels = [str(month) for month in month_counts.keys()]
    policy_counts = list(month_counts.values())

    plt.figure(figsize=(10, 6))  
    plt.bar(month_labels, policy_counts)
    plt.xlabel("Month")
    plt.ylabel("Number of Policies")
    plt.title("Policies Created by Month (This Year)")
    plt.xticks(rotation=45)  
    plt.grid(axis='y', linestyle='--', alpha=0.7)  

    fig = plt.gcf()
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    url = parse.quote(string)
    return url
    
