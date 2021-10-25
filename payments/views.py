import datetime

from django.shortcuts import render

from payments.models import Payments
from providers.models import Providers


def index(request):
    template_name = 'payments/index.html'
    trades = (
        ('baixinho', 'Baixinho Lanches'),
        ('escola', 'Escola Mais'),
        ('mari', 'Marinaul'),
    )
    providers = Providers.objects.all()
    context = {
        'providers': providers
    }
    return render(request, template_name, context)


def choice_trade(request):
    template_name = 'payments/index.html'
    provider = request.GET.get('provider')
    payments = Payments.objects.filter(provider=provider)
    context = {
        'payments': payments,
        'provider': payments.first().provider
    }
    return render(request, template_name, context)


def calculate(request):
    template_name = 'payments/index.html'
    payment_id = request.GET.get('payment_id')
    payment = Payments.objects.get(id=payment_id)
    try:
        original_value = float(payment.original_value.replace(',', '.'))
    except:
        original_value = float(payment.original_value)
    date_now = datetime.datetime.now()
    date_due_date = payment.due_date
    difference_of_days = (date_due_date - date_now.date()).days
    fees = (3 * 1 / 100)
    # NOVO_VALOR = VALOR_ORIGINAL - (VALOR_ORIGINAL * ((3 % / 30) * DIFERENCA_DE_DIAS))
    # 1000 - (1000 * (((3*1/100) / 30) * 16))
    value_new = original_value - (original_value * ((fees / 30) * difference_of_days))
    discount = original_value - value_new
    provider = payment.provider
    context = {
        'value_new': value_new,
        'payment': payment,
        'difference_of_days': difference_of_days,
        'date_now': date_now,
        'fees': fees,
        'discount': discount,
        'provider': provider
    }
    return render(request, template_name, context)
