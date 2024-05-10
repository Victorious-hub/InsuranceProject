from django.contrib import admin

from .models import (
    Answer, 
    Contacts, 
    Coupon, 
    InsuranceType, 
    InsuranceObject, 
    InsuranceRisk, 
    Contract, 
    News, 
    Policy, 
    Agent, 
    PrivacyPolicy, 
    Question, 
    Vacancy
)

@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    list_display = ('id', 'client', 'affiliate', 'insurance_type', 'insurance_object',)
    list_display_links = ('client',)
    list_filter = ('client', 'affiliate', 'insurance_type', 'insurance_object', 'insurance_risk',)
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

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'content',)
    list_display_links = ('title',)
    list_filter = ('title', 'content',)
    empty_value_display = "undefined"

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'text',)
    list_display_links = ('text',)
    list_filter = ('text',)
    empty_value_display = "undefined"

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'question',)
    list_display_links = ('text',)
    list_filter = ('text', 'question',)
    empty_value_display = "undefined"

admin.site.register(InsuranceObject)
admin.site.register(InsuranceRisk)
admin.site.register(InsuranceType)

admin.site.register(PrivacyPolicy)
admin.site.register(Contacts)
admin.site.register(Vacancy)