from django.contrib import admin
from .models import Affiliate, Agent, Client, CustomUser


@admin.register(CustomUser)
class CustomAccountAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'first_name', 'last_name',
                    'is_client', 'is_active', 'is_staff', 'created_at', 'updated_at',
                    )
    search_fields = ('first_name', 'email',)
    list_editable = ('is_active', 'is_staff', 'first_name', 'last_name',)

    list_filter = ('email',)
    empty_value_display = "undefined"


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'address', 'phone',
                    'balance',
                    )
    list_display_links = ('user',)

    list_filter = ('user', 'address', 'phone', 'balance',)

@admin.register(Agent)
class AgentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'affiliate', 'salary', 'tariff_rate',)
    list_display_links = ('user',)

    list_filter = ('user',)
    empty_value_display = "undefined"

admin.site.register(Affiliate)