from django.urls import path
from . import views

app_name = 'recommendations'

urlpatterns = [
    path('', views.recommendations_view, name='recommendations'),
    # Puedes agregar más rutas específicas para las recomendaciones aquí
]