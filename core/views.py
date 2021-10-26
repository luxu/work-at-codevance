import datetime

from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render

from payments.models import Payments
from .forms import LoginForm


def index(request):
    template_name = 'core/index.html'
    payments = Payments.objects.filter(decision=3)
    context = {
        'payments': payments
    }
    return render(request, template_name, context)


def choice_payment(request):
    template_name = 'core/index.html'
    payment_id = request.GET.get('payment')
    payment = Payments.objects.get(id=payment_id)
    context = {
        'payment': payment,
    }
    return render(request, template_name, context)


def calculate(request):
    template_name = 'core/index.html'
    decision = request.GET.get('decision')
    payment_id = request.GET.get('payment_id')
    payment = Payments.objects.get(id=payment_id)
    if int(decision):
        try:
            original_value = float(payment.original_value.replace(',', '.'))
        except:
            original_value = float(payment.original_value)
        date_now = datetime.datetime.now()
        date_due_date = payment.due_date
        difference_of_days = (date_due_date - date_now.date()).days
        fees = (3 * 1 / 100)
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
        payment.decision = Payments.APROVADOS
        payment.discount_value = discount
        payment.value_new = value_new
        payment.advance_date = date_now
        payment.save()
    else:
        payment.decision = Payments.NEGADOS
        context = {}
        payment.save()
    return render(request, template_name, context)


def login_view(request):
    loginForm = LoginForm()
    message = None

    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        loginForm = LoginForm(request.POST)
        if loginForm.is_valid():
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                _next = request.GET.get('next')
                if _next is not None:
                    return redirect(_next)
                else:
                    return redirect('/')
            else:
                message = {
                    'type': 'danger',
                    'text': 'Dados incorretos!'
                }
    context = {
        'form': loginForm,
        'message': message,
        'title': 'Login',
        'button_text': 'Entrar',
        'link_text': 'Registrar',
        'link_href': '/register'
    }
    return render(
        request,
        template_name='auth/auth.html',
        context=context,
        status=200
    )


def logout_view(request):
    logout(request)
    return redirect('/login')
