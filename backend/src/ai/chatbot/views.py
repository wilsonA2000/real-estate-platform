from django.http import HttpResponse

def chatbot_view(request):
    return HttpResponse("Chatbot endpoint")