import requests

def get_cat_info():
    response = requests.get('https://catfact.ninja/fact')
    return response.json()

def get_age():
    response = requests.get('https://api.agify.io/?name=Victor')
    return response.json()

print(get_cat_info())
print(get_age())