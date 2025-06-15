from django import forms
from .models import Property, PropertyPhoto
from apps.contact.models import ContactRequest  # Importar el modelo para ContactRequest

class PropertyForm(forms.ModelForm):
    """
    Formulario para crear y actualizar propiedades.
    """
    # Campo combinado para video (archivo o URL)
    video_content = forms.CharField(
        label="Video de la propiedad",
        required=False,
        widget=forms.TextInput(attrs={
            "class": "w-full p-2 bg-gray-800 text-white border border-gray-600 rounded",
            "placeholder": "Pega una URL de YouTube/Vimeo o sube un archivo de video"
        })
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Traducciones para los campos
        self.fields['title'].label = "Título"
        self.fields['description'].label = "Descripción"
        self.fields['location'].label = "Ubicación (Barrio/Zona)"
        self.fields['exact_address'].label = "Dirección exacta"
        self.fields['price'].label = "Precio"
        self.fields['currency'].label = "Moneda"
        self.fields['property_type'].label = "Tipo de propiedad"
        self.fields['requirements'].label = "Requisitos"
        self.fields['characteristics'].label = "Características"
        self.fields['bedrooms'].label = "Habitaciones"
        self.fields['bathrooms'].label = "Baños"
        self.fields['parking_spaces'].label = "Parqueaderos"
        self.fields['construction_area'].label = "Área construida (m²)"
        self.fields['land_area'].label = "Área total (m²)"
        
        # Ocultar los campos originales de video
        self.fields['video'].widget = forms.HiddenInput()
        self.fields['video_url'].widget = forms.HiddenInput()
        
        # Hacer que latitude y longitude no sean requeridos
        self.fields['latitude'].required = False
        self.fields['longitude'].required = False
        
        # Inicializar el campo video_content con el valor existente
        if self.instance and self.instance.pk:
            if self.instance.video_url:
                self.fields['video_content'].initial = self.instance.video_url
    class Meta:
        model = Property
        fields = [
            "title",
            "description",
            "location",
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
            "latitude",
            "longitude",
        ]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4, "class": "w-full p-2 bg-gray-800 text-white border border-gray-600 rounded"}),
            "requirements": forms.Textarea(attrs={"rows": 3, "class": "w-full p-2 bg-gray-800 text-white border border-gray-600 rounded"}),
            "characteristics": forms.Textarea(attrs={"rows": 3, "class": "w-full p-2 bg-gray-800 text-white border border-gray-600 rounded"}),
            "title": forms.TextInput(attrs={"class": "w-full p-2 bg-gray-800 text-white border border-gray-600 rounded"}),
            "location": forms.TextInput(attrs={"class": "w-full p-2 bg-gray-800 text-white border border-gray-600 rounded", "placeholder": "Ej: Centro, Chapinero, Poblado"}),
            "exact_address": forms.TextInput(attrs={"class": "w-full p-2 bg-gray-800 text-white border border-gray-600 rounded", "id": "exact_address"}),
            "price": forms.NumberInput(attrs={"class": "w-full p-2 bg-gray-800 text-white border border-gray-600 rounded", "step": "0.01"}),
            "currency": forms.Select(attrs={"class": "w-full p-2 bg-gray-800 text-white border border-gray-600 rounded"}),
            "property_type": forms.Select(attrs={"class": "w-full p-2 bg-gray-800 text-white border border-gray-600 rounded"}),
            "latitude": forms.HiddenInput(attrs={"id": "id_latitude"}),  # Configurado como campo oculto
            "longitude": forms.HiddenInput(attrs={"id": "id_longitude"}),  # Configurado como campo oculto
        }

    def clean(self):
        cleaned_data = super().clean()
        
        # Procesar el campo combinado de video
        video_content = cleaned_data.get("video_content")
        
        if video_content:
            # Verificar si es una URL
            if video_content.startswith('http'):
                cleaned_data["video_url"] = video_content
                cleaned_data["video"] = None
            # Si no es URL, debe ser un archivo (se procesará en la vista)
        elif self.instance and self.instance.pk and self.instance.video_url:
            # Mantener la URL de video existente si no se proporciona una nueva
            cleaned_data["video_url"] = self.instance.video_url
        
        # Validar tipo de archivo si se carga video
        video = cleaned_data.get("video")
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

        # Validar que latitude y longitude sean válidos si están presentes
        latitude = cleaned_data.get("latitude")
        longitude = cleaned_data.get("longitude")
        
        if latitude:
            try:
                # Limitar a 2 dígitos enteros y 6 decimales
                latitude = round(float(latitude), 6)
                if latitude < -90 or latitude > 90:
                    raise forms.ValidationError("La latitud debe estar entre -90 y 90.")
                cleaned_data["latitude"] = latitude
            except (ValueError, TypeError):
                cleaned_data["latitude"] = None
                
        if longitude:
            try:
                # Limitar a 3 dígitos enteros y 6 decimales
                longitude = round(float(longitude), 6)
                if longitude < -180 or longitude > 180:
                    raise forms.ValidationError("La longitud debe estar entre -180 y 180.")
                cleaned_data["longitude"] = longitude
            except (ValueError, TypeError):
                cleaned_data["longitude"] = None

        return cleaned_data

    def save(self, commit=True, *args, **kwargs):
        # Asegurar que latitude y longitude se guarden en el modelo
        instance = super().save(commit=False)
        
        # Guardar coordenadas solo si se proporcionan nuevas
        if self.cleaned_data.get("latitude") is not None and self.cleaned_data.get("longitude") is not None:
            instance.latitude = self.cleaned_data["latitude"]
            instance.longitude = self.cleaned_data["longitude"]
        elif self.instance and self.instance.pk:
            # Mantener las coordenadas existentes en caso de edición
            if self.instance.latitude and self.instance.longitude:
                instance.latitude = self.instance.latitude
                instance.longitude = self.instance.longitude
                
        # Guardar URL de video si existe
        if self.cleaned_data.get("video_url"):
            instance.video_url = self.cleaned_data["video_url"]
        elif self.instance and self.instance.pk and self.instance.video_url:
            # Mantener la URL de video existente
            instance.video_url = self.instance.video_url
            
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