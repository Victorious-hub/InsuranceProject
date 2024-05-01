from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Contract, InsuranceType

admin.site.register(Contract)
admin.site.register(InsuranceType)