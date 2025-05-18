from django.urls import path
from . import views

app_name = 'webhooks'

urlpatterns = [
    path('', views.webhook_view, name='webhook'),
    # Puedes agregar más rutas específicas para webhooks aquí
]