from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name="index_payments"),
    path('list_payments', views.list_payments, name="list_payments"),
    path('add_payments', views.add_payments, name="add_payments"),
    path('advance_request/<int:id>/', views.advance_request, name="advance_request"),
]
