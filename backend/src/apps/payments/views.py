# apps/payments/views.py
from django.shortcuts import render

def payments_list_view(request):
    # Aquí puedes agregar la lógica para obtener y mostrar los pagos
    return render(request, 'payments/payments_list.html')  # Asegúrate de tener esta plantilla