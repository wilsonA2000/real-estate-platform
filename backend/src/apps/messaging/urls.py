from django.urls import path
from . import views

urlpatterns = [
    path("", views.inbox, name="inbox"),  # Bandeja de entrada
    path("sent/", views.sent, name="sent"),  # Bandeja de enviados
    path("compose/", views.compose, name="compose"),  # Redactar correo
    path(
        "view/<int:message_id>/", views.view_message, name="view_message"
    ),  # Ver mensaje
    path(
        "reply/<int:message_id>/", views.reply_message, name="reply_message"
    ),  # Responder mensaje
    path(
        "mark-as-read/<int:message_id>/", views.mark_as_read, name="mark_as_read"
    ),  # Marcar como leído
    path(
        "delete/<int:message_id>/", views.delete_message, name="delete_message"
    ),  # Eliminar mensaje
]
