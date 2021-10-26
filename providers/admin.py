from django.contrib import admin

from providers.models import Providers


@admin.register(Providers)
class ProvidersAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'corporate_name',
        'cnpj',
    ]
