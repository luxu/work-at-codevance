from django.contrib import admin

from payments.models import Payments


@admin.register(Payments)
class PaymentsAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'provider',
        'due_date',
        'advance_date',
        'original_value',
        'discount_value',
        'value_new',
        'decision',
    ]
    list_filter = [
        'provider',
        'decision',
    ]
