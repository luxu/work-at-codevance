from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

from core.views import send_email_movement
from providers.models import Providers
from .forms import PaymentsForm
from .models import Payments, PaymentsLogs


def index(request):
    template_name = 'core/index.html'
    payments = Providers.objects.get(user=request.user.id)
    context = {
        'payments': payments.payments_set.all()
    }
    return render(request, template_name, context)


def advance_request(request, id):
    payment = Payments.objects.get(id=id)
    payment.decision = Payments.AGUARDANDO_CONFIRMACAO
    payment.save()
    send_email_movement(request, payment)
    logs = PaymentsLogs()
    logs.objects.create(
        payment=payment.payment,
        issue_date=payment.issue_date,
        due_date=payment.due_date,
        original_value=payment.original_value,
        decision=payment.decision,
        discount_value=payment.discount_value,
        value_new=payment.value_new,
    )
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
            return HttpResponseRedirect('/payments/list_payments')
    else:
        form = PaymentsForm()
    context = {
        'form': form
    }
    return render(request, template_name, context)
