from django.db import models
from django.conf import settings
from apps.properties.models import Property

class ContactRequest(models.Model):
    property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name='contact_requests',
        verbose_name="Propiedad"
    )
    tenant = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='contact_requests',
        verbose_name="Arrendatario"
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='received_contact_requests',
        verbose_name="Propietario"
    )
    message = models.TextField(
        verbose_name="Mensaje",
        help_text="Mensaje del arrendatario al propietario."
    )
    email = models.EmailField(
        blank=True,
        null=True,
        verbose_name="Correo electrónico",
        help_text="Correo electrónico del arrendatario (opcional)."
    )
    phone = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        verbose_name="Teléfono",
        help_text="Número de teléfono del arrendatario (opcional)."
    )
    is_read = models.BooleanField(
        default=False,
        verbose_name="Leído",
        help_text="Indica si el propietario ha leído la solicitud."
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de creación"
    )

    def __str__(self):
        return f'Solicitud de {self.tenant} para {self.property}'

    class Meta:
        verbose_name = "Solicitud de contacto"
        verbose_name_plural = "Solicitudes de contacto"
        ordering = ['-created_at']