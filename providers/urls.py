from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index_providers"),
    path('add_providers', views.add_providers, name="add_providers"),
    path('edit_providers/<int:id>/', views.edit_providers, name="edit_providers"),
    path('delete_providers/<int:id>/', views.delete_providers, name="delete_providers"),
]
