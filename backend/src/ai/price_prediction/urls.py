from django.urls import path
from . import views

app_name = 'price_prediction'

urlpatterns = [
    path('', views.price_prediction_view, name='price_prediction'),
    # Puedes agregar más rutas específicas para la predicción de precios aquí
]