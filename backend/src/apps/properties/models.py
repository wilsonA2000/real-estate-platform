from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class InterviewCode(models.Model):
    code = models.CharField(max_length=10, unique=True)
    profile_type = models.CharField(
        max_length=20,
        choices=[
            ("arrendatario", "Arrendatario"),
            ("arrendador", "Arrendador"),
            ("prestador", "Prestador"),
        ],
    )
    is_used = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.code


class Property(models.Model):
    PROPERTY_TYPES = [
        ("casa", "Casa"),
        ("apartamento", "Apartamento"),
        ("local", "Local"),
        ("habitacion", "Habitación"),
    ]

    CURRENCIES = [
        ("COP", "COP"),
        ("USD", "USD"),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=200)
    exact_address = models.CharField(max_length=200, blank=True, null=True)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=3, choices=CURRENCIES, default="COP")
    property_type = models.CharField(max_length=20, choices=PROPERTY_TYPES)
    video = models.FileField(
        upload_to="property_videos/",
        blank=True,
        null=True,
        help_text="Video de la propiedad (máximo 3 minutos, formatos .mp4, .mov o .avi)",
    )
    video_url = models.URLField(
        blank=True, null=True, help_text="URL de video alternativa (YouTube o Vimeo)"
    )
    requirements = models.TextField(blank=True)
    characteristics = models.TextField(blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="properties")
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    bedrooms = models.PositiveIntegerField(blank=True, null=True)
    bathrooms = models.PositiveIntegerField(blank=True, null=True)
    parking_spaces = models.PositiveIntegerField(blank=True, null=True)
    construction_area = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    land_area = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    main_photo = models.ImageField(upload_to="property_main_photos/", blank=True, null=True)

    def __str__(self):
        return self.title


class PropertyPhoto(models.Model):
    property = models.ForeignKey(
        Property, on_delete=models.CASCADE, related_name="related_photos"
    )
    image = models.ImageField(upload_to="property_photos/", blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Foto de {self.property.title}"