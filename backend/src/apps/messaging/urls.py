from django.urls import path
from . import views

urlpatterns = [
    path('inbox/', views.inbox, name='inbox'),
    path('sent/', views.sent, name='sent'),
    path('compose/', views.compose, name='compose'),
    path('message/<int:message_id>/', views.view_message, name='view_message'),
    path('reply/<int:message_id>/', views.reply, name='reply'),
    path('delete/<int:message_id>/', views.delete_message, name='delete_message'),
]