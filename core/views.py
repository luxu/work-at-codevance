import datetime

from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from payments.models import Payments, PaymentsLogs
from .forms import LoginForm


def index(request):
    if request.user.is_superuser:
        template_name = 'auth/index.html'
        payments = Payments.objects.filter(decision=3)
    else:
        template_name = 'index.html'
        payments = Payments.objects.filter(decision=3)
    context = {
        'payments': payments
    }
    return render(request, template_name, context)


def choice_payment(request):
    template_name = 'auth/index.html'
    payment_id = request.GET.get('payment')
    payment = Payments.objects.get(id=payment_id)
    provider = payment.provider
    context = {
        'payment': payment,
        'provider': provider,
    }
    return render(request, template_name, context)


def calculate(request):
    template_name = 'auth/index.html'
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
        payment.decision = Payments.ANTECIPADO
        payment.discount_value = discount
        payment.value_new = value_new
        payment.advance_date = date_now
        payment.save()
    else:
        payment.decision = Payments.NEGADO
        context = {}
        payment.save()
    send_email_movement(request, payment)
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
        # 'link_text': 'Registrar',
        # 'link_href': '/register'
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


def send_email_movement(request, payment):
    decision = [r[1] for r in payment.DECISION_STATUS if r[0] == payment.decision]
    context = {
        'payment': payment,
        'decision': decision[0]
    }
    try:
        html_message = render_to_string(
            'payments/email.html',
            context
        )
        message = strip_tags(html_message)
        send_mail(
            subject="Solicitação de Recebíveis",
            message=message,
            html_message=html_message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[
                request.user.email
            ],
            fail_silently=False,
        )
        logs = PaymentsLogs(
            provider=payment.provider,
            issue_date=payment.issue_date,
            due_date=payment.due_date,
            original_value=payment.original_value,
            decision=payment.decision,
            discount_value=payment.discount_value,
            value_new=payment.value_new,
        )
        logs.save()
    except Exception:
        pass
