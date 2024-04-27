from django.contrib import admin
from .models import Affiliate, Agent, CustomUser, Client
from django.contrib.auth.admin import UserAdmin

class EmployeeAdmin(admin.ModelAdmin):
    pass

admin.site.register(Agent, EmployeeAdmin)
admin.site.register(CustomUser)
admin.site.register(Client)
admin.site.register(Affiliate)