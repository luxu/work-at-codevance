from django.http import HttpResponseRedirect
from django.shortcuts import render

from providers.models import Providers
from .forms import PaymentsForm
from .models import Payments


def index(request):
    template_name = 'index.html'
    payments = Providers.objects.get(user=request.user.id)
    context = {
        'payments': payments.payments_set.all()
    }
    return render(request, template_name, context)


def advance_request(request, id):
    payments = Payments.objects.get(id=id)
    payments.decision = Payments.AGUARDANDO_LIBERACAO
    payments.save()
    return HttpResponseRedirect('/payments')


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
            return HttpResponseRedirect('/payments/')
    else:
        form = PaymentsForm()
    context = {
        'form': form
    }
    return render(request, template_name, context)
