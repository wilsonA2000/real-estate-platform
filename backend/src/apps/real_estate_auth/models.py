from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class CustomUser(AbstractUser):
    # Opciones actualizadas a español
    PROFILE_CHOICES = (
        ("arrendador", "Arrendador"),
        ("arrendatario", "Arrendatario"),
        ("prestador", "Prestador de Servicios"),
    )

    # Campos base (username, password, etc. heredados de AbstractUser)

    # Campos adicionales
    name = models.CharField(
        _("nombre completo"), max_length=255, help_text=_("Ingrese su nombre completo")
    )
    email = models.EmailField(
        _("correo electrónico"),
        unique=True,
        error_messages={"unique": _("Este correo electrónico ya está registrado.")},
    )
    profile_type = models.CharField(
        _("tipo de perfil"),
        max_length=20,
        choices=PROFILE_CHOICES,
        default="arrendatario",
        help_text=_("Seleccione su rol en la plataforma"),
    )
    phone_number = models.CharField(
        _("teléfono"),
        max_length=20,
        blank=True,
        null=True,
        help_text=_("Número de contacto opcional"),
    )
    profile_picture = models.ImageField(
        _("foto de perfil"),
        upload_to="profile_pics/",
        blank=True,
        null=True,
        help_text=_("Suba una imagen para su perfil"),
    )
    interview_code = models.CharField(
        _("código de entrevista"),
        max_length=10,
        blank=True,
        null=True,
        unique=True,
        help_text=_("Código asignado durante la entrevista por el administrador"),
    )
    rating = models.PositiveSmallIntegerField(
        _("calificación inicial"),
        default=0,
        help_text=_("Calificación de 1 a 5 asignada por el administrador"),
    )
    resume = models.TextField(
        _("hoja de vida"),
        blank=True,
        null=True,
        help_text=_("Información de la hoja de vida"),
    )

    # Configuraciones
    REQUIRED_FIELDS = ["email", "name", "profile_type"]  # Campos obligatorios

    # Métodos
    def __str__(self):
        return f"{self.get_full_name()} ({self.get_profile_type_display()})"

    def get_full_name(self):
        return self.name.strip()

    class Meta:
        verbose_name = _("usuario")
        verbose_name_plural = _("usuarios")
        ordering = ["-date_joined"]

    # Permisos personalizados (opcional)
    @property
    def is_arrendador(self):
        return self.profile_type == "arrendador"

    @property
    def is_arrendatario(self):
        return self.profile_type == "arrendatario"

    @property
    def is_prestador(self):
        return self.profile_type == "prestador"


class Contract(models.Model):
    parties = models.ManyToManyField(CustomUser, related_name="contracts")
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=50,
        default="active",
        choices=[
            ("active", "Activo"),
            ("terminated", "Terminado"),
            ("pending", "Pendiente"),
        ],
    )

    def __str__(self):
        return f"Contrato entre {', '.join(str(p) for p in self.parties.all())}"

    class Meta:
        verbose_name = _("contrato")
        verbose_name_plural = _("contratos")
        ordering = ["-created_at"]
