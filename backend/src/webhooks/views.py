from django.http import HttpResponse

def webhook_view(request):
    return HttpResponse("Webhook endpoint")