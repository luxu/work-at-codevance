from django.contrib import admin

from payments.models import Payments


@admin.register(Payments)
class PaymentsAdmin(admin.ModelAdmin):
    list_display = [
        'issue_date',
        'due_date',
        'original_value',
    ]

# admin.site.register(Payments, PaymentsAdmin)
