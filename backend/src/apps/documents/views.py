from django.shortcuts import render
from .models import Document

def documents_list_view(request):
    documents = Document.objects.all()  # Obtiene todos los documentos de la base de datos
    return render(request, 'documents/documents_list.html', {'documents': documents})