from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Contract

admin.site.register(Contract)