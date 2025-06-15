# src/apps/contact/views.py - Añadir a la función process_contact_request
from apps.notifications.models import Notification

# Después de guardar la solicitud de contacto
Notification.objects.create(
    user=contact_request.owner,
    type='contact_request',
    title='Nueva solicitud de contacto',
    message=f'{contact_request.tenant.name} está interesado en tu propiedad {contact_request.property.title}',
    related_object_id=contact_request.id,
    related_object_type='ContactRequest',
    url=f'/contact-requests/tenant/{contact_request.tenant.id}/request/{contact_request.id}/'
)
