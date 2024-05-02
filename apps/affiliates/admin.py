from django.contrib import admin

from .models import InsuranceType, InsuranceObject, InsuranceRisk, Contract, Pollis

admin.site.register(InsuranceType)
admin.site.register(InsuranceObject)
admin.site.register(InsuranceRisk)
admin.site.register(Contract)
admin.site.register(Pollis)