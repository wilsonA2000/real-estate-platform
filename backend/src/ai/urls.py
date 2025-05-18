from django.urls import path, include

app_name = 'ai'

urlpatterns = [
    path('chatbot/', include('ai.chatbot.urls')),
    path('image-analysis/', include('ai.image_analysis.urls')),
    path('price-prediction/', include('ai.price_prediction.urls')),
    path('recommendations/', include('ai.recommendations.urls')),
]