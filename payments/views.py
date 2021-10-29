import datetime

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

from core.views import send_email_movement
from providers.models import Providers
from .forms import PaymentsForm
from .models import Payments, PaymentsLogs


def index(request):
    template_name = 'core/index.html'
    payments = Providers.objects.get(user=request.user.id)
    payments = payments.payments_set.all()
    date_today = datetime.datetime.now().date()
    list_payments = []
    for payment in payments:
        difference_of_days = (payment.due_date - date_today).days
        if difference_of_days == 0:
            payment.decision = 4
            payment.save()
        list_payments.append(payment)
    context = {
        'payments': list_payments
    }
    return render(request, template_name, context)


def advance_request(request, id):
    payment = Payments.objects.get(id=id)
    payment.decision = Payments.AGUARDANDO_CONFIRMACAO
    payment.save()
    send_email_movement(request, payment)
    return redirect('/payments/')


@login_required
def list_payments(request):
    template_name = 'payments/list_payments.html'
    payments = Payments.objects.all()
    context = {
        'payments': payments
    }
    return render(request, template_name, context)


def add_payments(request):
    template_name = 'payments/form_payments.html'
    if request.method == 'POST':
        form = PaymentsForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.decision = 0
            obj.save()
            send_email_movement(request, obj)
            return HttpResponseRedirect('/payments/list_payments')
    else:
        form = PaymentsForm()
    context = {
        'form': form
    }
    return render(request, template_name, context)


def logs(request):
    template_name = 'payments/logs.html'
    logs = PaymentsLogs.objects.all()
    context = {
        'logs': logs
    }
    return render(request, template_name, context)
