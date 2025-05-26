from django import forms
from .models import Property, PropertyPhoto


class PropertyForm(forms.ModelForm):
    """
    Formulario para crear y actualizar propiedades.
    """

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
            "main_photo",
        ]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4}),
            "requirements": forms.Textarea(attrs={"rows": 3}),
            "characteristics": forms.Textarea(attrs={"rows": 3}),
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

        return cleaned_data


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
            if not image.content_type or not image.content_type.startswith("image/"):
                raise forms.ValidationError("El archivo debe ser una imagen válida.")

        return image