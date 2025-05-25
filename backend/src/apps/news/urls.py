# apps/news/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.news_list_view, name='news'),  # Ruta principal para la vista de noticias
]