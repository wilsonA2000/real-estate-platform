from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
import random
import string


class InterviewCode(models.Model):
    """
    Modelo para los códigos de entrevista que se requieren para el registro.
    """
    code = models.CharField(
        max_length=10, 
        unique=True, 
        verbose_name=_("Código de entrevista")
    )
    profile_type = models.CharField(
        max_length=20,
        choices=[
            ("arrendador", "Arrendador"),
            ("arrendatario", "Arrendatario"),
            ("prestador", "Prestador de Servicios"),
        ],
        verbose_name=_("Tipo de perfil")
    )
    rating = models.PositiveSmallIntegerField(
        default=0,
        verbose_name=_("Calificación inicial"),
        help_text=_("Calificación de 1 a 5 asignada por el administrador")
    )
    is_used = models.BooleanField(
        default=False,
        verbose_name=_("Utilizado"),
        help_text=_("Indica si el código ya ha sido utilizado para registrarse")
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Fecha de creación")
    )
    created_by = models.ForeignKey(
        'CustomUser',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_codes",
        verbose_name=_("Creado por")
    )
    notes = models.TextField(
        blank=True,
        null=True,
        verbose_name=_("Notas"),
        help_text=_("Notas adicionales sobre la entrevista")
    )

    class Meta:
        verbose_name = _("Código de entrevista")
        verbose_name_plural = _("Códigos de entrevista")
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.code} - {self.get_profile_type_display()}"
    
    @classmethod
    def generate_code(cls):
        """
        Genera un código único de 8 caracteres alfanuméricos.
        """
        while True:
            code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
            if not cls.objects.filter(code=code).exists():
                return code


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
    is_verified = models.BooleanField(
        _("verificado"),
        default=False,
        help_text=_("Indica si el usuario ha sido verificado por un administrador")
    )
    verification_date = models.DateTimeField(
        _("fecha de verificación"),
        null=True,
        blank=True,
        help_text=_("Fecha en que el usuario fue verificado")
    )
    verified_by = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="verified_users",
        verbose_name=_("Verificado por"),
        help_text=_("Administrador que verificó al usuario")
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