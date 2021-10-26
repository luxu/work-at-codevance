from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('choice_payment', views.choice_payment, name="choice_payment"),
    path('calculate', views.calculate, name="calculate"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name='logout'),
]
