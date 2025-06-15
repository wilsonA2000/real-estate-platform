from django import forms
from .models import Property, PropertyPhoto
from apps.contact.models import ContactRequest  # Importar el modelo para ContactRequest

class PropertyForm(forms.ModelForm):
    """
    Formulario para crear y actualizar propiedades.
    """
    class Meta:
        model = Property
        fields = [
            "title",
            "description",
            "exact_address",
            "price",
            "currency",
            "property_type",
            "video",
            "video_url",
            "requirements",
            "characteristics",
            "bedrooms",
            "bathrooms",
            "parking_spaces",
            "construction_area",
            "land_area",
            "main_photo",
            "latitude",  # Agregado para incluir en el formulario
            "longitude",  # Agregado para incluir en el formulario
        ]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4, "class": "w-full p-2 bg-gray-800 text-white border border-gray-600 rounded"}),
            "requirements": forms.Textarea(attrs={"rows": 3, "class": "w-full p-2 bg-gray-800 text-white border border-gray-600 rounded"}),
            "characteristics": forms.Textarea(attrs={"rows": 3, "class": "w-full p-2 bg-gray-800 text-white border border-gray-600 rounded"}),
            "title": forms.TextInput(attrs={"class": "w-full p-2 bg-gray-800 text-white border border-gray-600 rounded"}),
            "exact_address": forms.TextInput(attrs={"class": "w-full p-2 bg-gray-800 text-white border border-gray-600 rounded", "id": "exact_address"}),
            "price": forms.NumberInput(attrs={"class": "w-full p-2 bg-gray-800 text-white border border-gray-600 rounded", "step": "0.01"}),
            "latitude": forms.HiddenInput(attrs={"id": "latitude"}),  # Configurado como campo oculto
            "longitude": forms.HiddenInput(attrs={"id": "longitude"}),  # Configurado como campo oculto
        }

    def clean(self):
        cleaned_data = super().clean()

        video = cleaned_data.get("video")
        video_url = cleaned_data.get("video_url")

        # Validar que no se proporcionen video y video_url simultáneamente
        if video and video_url:
            raise forms.ValidationError(
                "Solo puede proporcionar un video o una URL de video, no ambos."
            )

        # Validar tipo de archivo si se carga video
        if video:
            valid_extensions = [".mp4", ".mov", ".avi"]
            if not any(video.name.lower().endswith(ext) for ext in valid_extensions):
                raise forms.ValidationError("El video debe tener formato .mp4, .mov o .avi.")
            if video.size > 50 * 1024 * 1024:  # Limitar a 50MB
                raise forms.ValidationError("El video no puede superar los 50 MB.")

        # Validar que el precio sea positivo
        price = cleaned_data.get("price")
        if price is not None and price <= 0:
            raise forms.ValidationError("El precio debe ser mayor a 0.")

        # Validar que latitude y longitude estén presentes y sean válidos
        latitude = cleaned_data.get("latitude")
        longitude = cleaned_data.get("longitude")
        if latitude is not None and longitude is not None:
            if latitude < -90 or latitude > 90 or longitude < -180 or longitude > 180:
                raise forms.ValidationError("Las coordenadas de latitud deben estar entre -90 y 90, y las de longitud entre -180 y 180.")
        elif latitude is None or longitude is None:
            # Permitir que sean nulos si no se proporcionan (según el modelo)
            pass
        else:
            raise forms.ValidationError("Debes proporcionar ambas coordenadas (latitud y longitud) o ninguna.")

        return cleaned_data

    def save(self, commit=True, *args, **kwargs):
        # Asegurar que latitude y longitude se guarden en el modelo
        instance = super().save(commit=False)
        if self.cleaned_data.get("latitude") is not None and self.cleaned_data.get("longitude") is not None:
            instance.latitude = self.cleaned_data["latitude"]
            instance.longitude = self.cleaned_data["longitude"]
        if commit:
            instance.save()
        return instance


class PropertyPhotoForm(forms.ModelForm):
    """
    Formulario para cargar imágenes de las propiedades.
    """
    class Meta:
        model = PropertyPhoto
        fields = ["image"]

    def clean_image(self):
        image = self.cleaned_data.get("image")

        if image:
            if image.size > 5 * 1024 * 1024:  # Limitar tamaño máximo a 5MB
                raise forms.ValidationError("La imagen no puede superar los 5 MB.")
            valid_extensions = [".jpg", ".jpeg", ".png"]
            if not any(image.name.lower().endswith(ext) for ext in valid_extensions):
                raise forms.ValidationError("La imagen debe tener formato .jpg, .jpeg o .png.")
            if not image.content_type or not image.content_type.startswith("image/"):
                raise forms.ValidationError("El archivo debe ser una imagen válida.")

        return image


class ContactRequestForm(forms.ModelForm):
    """
    Formulario para que el arrendatario haga solicitudes de contacto.
    """
    phone = forms.CharField(
        max_length=15,
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "Tu número de teléfono", "class": "w-full p-2 bg-gray-800 text-white border border-gray-600 rounded"})
    )
    email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={"placeholder": "Tu correo electrónico", "class": "w-full p-2 bg-gray-800 text-white border border-gray-600 rounded"})
    )

    class Meta:
        model = ContactRequest
        fields = ['message']  # Solo message se guarda en el modelo
        widgets = {
            'message': forms.Textarea(attrs={
                'rows': 4, 
                'class': 'w-full p-2 bg-gray-800 text-white border border-gray-600 rounded',
                'placeholder': 'Escribe tu mensaje para el propietario...'
            })
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and "@" not in email:
            raise forms.ValidationError("Ingrese un correo electrónico válido.")
        return email

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if phone and (not phone.isdigit() or len(phone) < 7 or len(phone) > 15):
            raise forms.ValidationError("Ingrese un número de teléfono válido (solo dígitos, 7-15 caracteres).")
        return phone