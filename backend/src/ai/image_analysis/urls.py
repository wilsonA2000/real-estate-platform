from django.urls import path
from . import views

app_name = 'image_analysis'

urlpatterns = [
    path('', views.image_analysis_view, name='image_analysis'),
    # Puedes agregar más rutas específicas para el análisis de imágenes aquí
]