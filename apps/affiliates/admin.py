from django.contrib import admin

from .models import Coupon, InsuranceType, InsuranceObject, InsuranceRisk, Contract, Policy

admin.site.register(InsuranceType)
admin.site.register(InsuranceObject)
admin.site.register(InsuranceRisk)
admin.site.register(Contract)
admin.site.register(Policy)
admin.site.register(Coupon)