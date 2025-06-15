from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from .models import ContactRequest
from apps.messaging.models import Message
from apps.properties.models import Property
from apps.notifications.models import Notification  # Import añadido

@login_required
@require_POST
def process_contact_request(request, request_id):
    """
    Procesa una solicitud de contacto (aceptar o rechazar)
    """
    contact_request = get_object_or_404(ContactRequest, id=request_id)
    
    # Verificar que el usuario actual es el propietario
    if request.user != contact_request.owner:
        messages.error(request, "No tienes permiso para procesar esta solicitud.")
        return redirect('inbox')
    
    action = request.POST.get('action')
    
    if action == 'accept':
        # Marcar como leída
        contact_request.is_read = True
        contact_request.save()
        
        # Crear notificación para el arrendador
        Notification.objects.create(
            user=contact_request.owner,
            type='contact_request',
            title='Nueva solicitud de contacto aceptada',
            message=f'{contact_request.tenant.name} está interesado en tu propiedad {contact_request.property.title} y has aceptado la solicitud.',
            related_object_id=contact_request.id,
            related_object_type='ContactRequest',
            url=f'/contact-requests/tenant/{contact_request.tenant.id}/request/{contact_request.id}/'
        )
        
        # Crear un mensaje automático para el arrendatario
        Message.objects.create(
            sender=request.user,
            recipient=contact_request.tenant,
            subject=f"Respuesta a tu solicitud sobre {contact_request.property.title}",
            body=f"Hola {contact_request.tenant.name},\n\nHe recibido tu solicitud sobre la propiedad '{contact_request.property.title}'. Me gustaría discutir más detalles contigo.\n\nSaludos,\n{request.user.name}"
        )
        
        # Enviar notificación por correo electrónico si hay email
        if contact_request.tenant.email:
            context = {
                'tenant_name': contact_request.tenant.name,
                'owner_name': request.user.name,
                'property_title': contact_request.property.title,
                'login_url': request.build_absolute_uri(reverse('login'))
            }
            
            html_message = render_to_string('contact/email/contact_accepted.html', context)
            plain_message = strip_tags(html_message)
            
            send_mail(
                f'Tu solicitud sobre {contact_request.property.title} ha sido aceptada',
                plain_message,
                settings.DEFAULT_FROM_EMAIL,
                [contact_request.tenant.email],
                html_message=html_message,
                fail_silently=True
            )
        
        messages.success(request, f"Has aceptado la solicitud de {contact_request.tenant.name}. Se ha enviado un mensaje automático.")
        return redirect('inbox')
    
    elif action == 'reject':
        # Marcar como leída
        contact_request.is_read = True
        contact_request.save()
        
        messages.info(request, f"Has rechazado la solicitud de {contact_request.tenant.name}.")
        return redirect('inbox')
    
    else:
        messages.error(request, "Acción no válida.")
        return redirect('inbox')

@login_required
def view_tenant_profile(request, tenant_id, request_id=None):
    """
    Ver el perfil de un arrendatario que ha enviado una solicitud
    """
    from django.contrib.auth import get_user_model
    User = get_user_model()
    
    tenant = get_object_or_404(User, id=tenant_id, profile_type='arrendatario')
    
    # Si se proporciona un ID de solicitud, marcarla como leída
    if request_id:
        contact_request = get_object_or_404(ContactRequest, id=request_id, owner=request.user)
        contact_request.is_read = True
        contact_request.save()
    
    context = {
        'tenant': tenant,
        'contact_request': contact_request if request_id else None
    }
    
    return render(request, 'contact/tenant_profile.html', context)

@login_required
def contact_requests(request):
    """
    Muestra todas las solicitudes de contacto para un arrendador
    """
    if request.user.profile_type != 'arrendador':
        messages.error(request, "Solo los arrendadores pueden ver solicitudes de contacto.")
        return redirect('inbox')
    
    contact_requests = ContactRequest.objects.filter(owner=request.user).order_by('-created_at')
    
    context = {
        'contact_requests': contact_requests,
        'unread_count': contact_requests.filter(is_read=False).count()
    }
    
    return render(request, 'contact/contact_requests.html', context)