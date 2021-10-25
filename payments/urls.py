from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('choice_trade', views.choice_trade, name="choice_trade"),
    path('calculate', views.calculate, name="calculate"),
]
