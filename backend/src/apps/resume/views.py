# resume/views.py
from django.shortcuts import render

def resume_view(request):
    # Aquí puedes pasar datos dinámicos si es necesario
    return render(request, "resume/resume.html")