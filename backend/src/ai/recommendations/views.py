from django.http import HttpResponse

def recommendations_view(request):
    return HttpResponse("Chatbot endpoint")