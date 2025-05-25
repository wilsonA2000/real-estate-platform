# apps/news/views.py
from django.shortcuts import render

def news_list_view(request):
    # Aquí puedes obtener las noticias desde la base de datos si tienes un modelo
    # Por ahora, vamos a pasar datos estáticos como ejemplo

    news_data = [
        {"title": "Noticia 1", "content": "Contenido de la noticia 1"},
        {"title": "Noticia 2", "content": "Contenido de la noticia 2"},
        {"title": "Noticia 3", "content": "Contenido de la noticia 3"},
    ]
    
    return render(request, 'news/news_list.html', {'news': news_data})