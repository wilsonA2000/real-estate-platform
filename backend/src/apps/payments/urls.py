# apps/payments/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.payments_list_view, name='payments'),  # Asegúrate de que esta ruta esté definida
]