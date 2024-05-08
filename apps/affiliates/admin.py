from django.contrib import admin

from .models import Coupon, InsuranceType, InsuranceObject, InsuranceRisk, Contract, Policy, Agent

@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    list_display = ('id', 'client', 'affiliate', 'insurance_type', 'insurance_object', 'is_completed',)
    list_display_links = ('client',)
    list_filter = ('client', 'affiliate', 'insurance_type', 'insurance_object', 'insurance_risk', 'is_completed',)
    empty_value_display = "undefined"

@admin.register(Policy)
class PolicyAdmin(admin.ModelAdmin):
    list_display = ('id', 'agent', 'contract', 'insurance_sum', 'start_date', 'end_date', 'price',)
    list_display_links = ('agent',)
    list_filter = ('agent', 'contract',)
    empty_value_display = "undefined"

@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ('id', 'code', 'discount', 'active',)
    list_display_links = ('code',)
    list_filter = ('code', 'active',)
    empty_value_display = "undefined"

admin.register(InsuranceObject)
admin.register(InsuranceRisk)
admin.register(InsuranceType)