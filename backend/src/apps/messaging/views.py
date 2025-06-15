from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages as django_messages
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib.auth import get_user_model

from .models import Message
from apps.contact.models import ContactRequest

User = get_user_model()

@login_required
def inbox(request):
    # Obtener mensajes recibidos no eliminados por el destinatario
    received_messages = Message.objects.filter(
        recipient=request.user, is_deleted_by_recipient=False
    )
    
    # Buscar mensajes si hay un parámetro de búsqueda
    search_query = request.GET.get('search', '')
    if search_query:
        received_messages = received_messages.filter(
            Q(subject__icontains=search_query) | 
            Q(body__icontains=search_query) |
            Q(sender__username__icontains=search_query) |
            Q(sender__name__icontains=search_query)
        )
    
    # Ordenar por fecha de creación (más recientes primero)
    received_messages = received_messages.order_by('-created_at')
    
    # Paginación
    paginator = Paginator(received_messages, 10)  # 10 mensajes por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Para arrendadores, obtener solicitudes de contacto no leídas
    contact_requests = None
    contact_requests_count = 0
    if request.user.profile_type == 'arrendador':
        contact_requests = ContactRequest.objects.filter(
            owner=request.user, is_read=False
        ).order_by('-created_at')[:5]  # Mostrar solo las 5 más recientes
        contact_requests_count = ContactRequest.objects.filter(
            owner=request.user, is_read=False
        ).count()
    
    context = {
        'received_messages': page_obj,
        'search_query': search_query,
        'unread_count': received_messages.filter(is_read=False).count(),
        'contact_requests': contact_requests,
        'contact_requests_count': contact_requests_count,
    }
    
    return render(request, 'messaging/inbox.html', context)

@login_required
def sent(request):
    # Obtener mensajes enviados no eliminados por el remitente
    sent_messages = Message.objects.filter(
        sender=request.user, is_deleted_by_sender=False
    )
    
    # Buscar mensajes si hay un parámetro de búsqueda
    search_query = request.GET.get('search', '')
    if search_query:
        sent_messages = sent_messages.filter(
            Q(subject__icontains=search_query) | 
            Q(body__icontains=search_query) |
            Q(recipient__username__icontains=search_query) |
            Q(recipient__name__icontains=search_query)
        )
    
    # Ordenar por fecha de creación (más recientes primero)
    sent_messages = sent_messages.order_by('-created_at')
    
    # Paginación
    paginator = Paginator(sent_messages, 10)  # 10 mensajes por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Contar mensajes no leídos para la barra lateral
    unread_count = Message.objects.filter(
        recipient=request.user, is_read=False, is_deleted_by_recipient=False
    ).count()
    
    # Para arrendadores, contar solicitudes de contacto no leídas
    contact_requests_count = 0
    if request.user.profile_type == 'arrendador':
        contact_requests_count = ContactRequest.objects.filter(
            owner=request.user, is_read=False
        ).count()
    
    context = {
        'sent_messages': page_obj,
        'search_query': search_query,
        'unread_count': unread_count,
        'contact_requests_count': contact_requests_count,
    }
    
    return render(request, 'messaging/sent.html', context)

@login_required
def view_message(request, message_id):
    # Obtener el mensaje y verificar que el usuario tenga permiso para verlo
    message = get_object_or_404(Message, id=message_id)
    
    # Verificar permisos
    if not ((message.recipient == request.user and not message.is_deleted_by_recipient) or 
            (message.sender == request.user and not message.is_deleted_by_sender)):
        django_messages.error(request, "No tienes permiso para ver este mensaje.")
        return redirect('inbox')
    
    # Marcar como leído si el usuario es el destinatario
    if request.user == message.recipient and not message.is_read:
        message.is_read = True
        message.save()
    
    # Contar mensajes no leídos para la barra lateral
    unread_count = Message.objects.filter(
        recipient=request.user, is_read=False, is_deleted_by_recipient=False
    ).count()
    
    # Para arrendadores, contar solicitudes de contacto no leídas
    contact_requests_count = 0
    if request.user.profile_type == 'arrendador':
        contact_requests_count = ContactRequest.objects.filter(
            owner=request.user, is_read=False
        ).count()
    
    context = {
        'message': message,
        'unread_count': unread_count,
        'contact_requests_count': contact_requests_count,
    }
    
    return render(request, 'messaging/view_message.html', context)

@login_required
def compose(request):
    # Obtener el destinatario si se proporciona en la URL
    recipient_id = request.GET.get('to')
    recipient = None
    if recipient_id:
        try:
            recipient = User.objects.get(id=recipient_id)
        except User.DoesNotExist:
            django_messages.error(request, "El destinatario seleccionado no existe.")
    
    if request.method == 'POST':
        recipient_id = request.POST.get('recipient')
        subject = request.POST.get('subject')
        body = request.POST.get('body')
        
        # Validar los datos
        if not recipient_id or not subject or not body:
            django_messages.error(request, "Por favor complete todos los campos.")
            return render(request, 'messaging/compose.html', {'recipient': recipient})
        
        try:
            recipient = User.objects.get(id=recipient_id)
        except User.DoesNotExist:
            django_messages.error(request, "El destinatario seleccionado no existe.")
            return render(request, 'messaging/compose.html', {'recipient': None})
        
        # Crear el mensaje
        Message.objects.create(
            sender=request.user,
            recipient=recipient,
            subject=subject,
            body=body
        )
        
        django_messages.success(request, f"Mensaje enviado a {recipient.name}.")
        return redirect('sent')
    
    # Contar mensajes no leídos para la barra lateral
    unread_count = Message.objects.filter(
        recipient=request.user, is_read=False, is_deleted_by_recipient=False
    ).count()
    
    # Para arrendadores, contar solicitudes de contacto no leídas
    contact_requests_count = 0
    if request.user.profile_type == 'arrendador':
        contact_requests_count = ContactRequest.objects.filter(
            owner=request.user, is_read=False
        ).count()
    
    # Obtener usuarios para el selector de destinatarios
    users = User.objects.exclude(id=request.user.id).order_by('name')
    
    context = {
        'users': users,
        'recipient': recipient,
        'unread_count': unread_count,
        'contact_requests_count': contact_requests_count,
    }
    
    return render(request, 'messaging/compose.html', context)

@login_required
def reply(request, message_id):
    # Obtener el mensaje original
    original_message = get_object_or_404(Message, id=message_id)
    
    # Verificar permisos
    if not (original_message.recipient == request.user or original_message.sender == request.user):
        django_messages.error(request, "No tienes permiso para responder a este mensaje.")
        return redirect('inbox')
    
    # Determinar el destinatario (el remitente del mensaje original)
    recipient = original_message.sender
    
    if request.method == 'POST':
        subject = request.POST.get('subject')
        body = request.POST.get('body')
        
        # Validar los datos
        if not subject or not body:
            django_messages.error(request, "Por favor complete todos los campos.")
            return render(request, 'messaging/reply.html', {'original_message': original_message})
        
        # Crear el mensaje de respuesta
        Message.objects.create(
            sender=request.user,
            recipient=recipient,
            subject=subject,
            body=body
        )
        
        django_messages.success(request, f"Respuesta enviada a {recipient.name}.")
        return redirect('inbox')
    
    # Contar mensajes no leídos para la barra lateral
    unread_count = Message.objects.filter(
        recipient=request.user, is_read=False, is_deleted_by_recipient=False
    ).count()
    
    # Para arrendadores, contar solicitudes de contacto no leídas
    contact_requests_count = 0
    if request.user.profile_type == 'arrendador':
        contact_requests_count = ContactRequest.objects.filter(
            owner=request.user, is_read=False
        ).count()
    
    # Preparar el asunto para la respuesta
    subject = original_message.subject
    if not subject.startswith('Re:'):
        subject = f"Re: {subject}"
    
    context = {
        'original_message': original_message,
        'recipient': recipient,
        'subject': subject,
        'unread_count': unread_count,
        'contact_requests_count': contact_requests_count,
    }
    
    return render(request, 'messaging/reply.html', context)

@login_required
def delete_message(request, message_id):
    # Obtener el mensaje
    message = get_object_or_404(Message, id=message_id)
    
    # Verificar que el usuario tenga permiso para eliminar el mensaje
    if message.sender != request.user and message.recipient != request.user:
        django_messages.error(request, "No tienes permiso para eliminar este mensaje.")
        return redirect('inbox')
    
    # Marcar como eliminado según corresponda
    if message.sender == request.user:
        message.is_deleted_by_sender = True
    if message.recipient == request.user:
        message.is_deleted_by_recipient = True
    
    # Si ambos usuarios han eliminado el mensaje, eliminarlo físicamente
    if message.is_deleted_by_sender and message.is_deleted_by_recipient:
        message.delete()
    else:
        message.save()
    
    django_messages.success(request, "Mensaje eliminado.")
    
    # Redirigir a la bandeja de entrada o a mensajes enviados según corresponda
    if message.recipient == request.user:
        return redirect('inbox')
    else:
        return redirect('sent')