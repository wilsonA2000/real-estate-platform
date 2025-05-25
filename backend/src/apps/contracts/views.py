from django.shortcuts import render

def contracts_list_view(request):
    # Aquí puedes obtener los contratos desde tu base de datos
    # y pasarlos a la plantilla.
    return render(request, 'contracts/contracts_list.html')