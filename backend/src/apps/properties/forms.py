from django import forms
from .models import Property, PropertyPhoto


class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = [
            "title",
            "description",
            "location",
            "price",
            "property_type",
            "video",
            "video_url",
            "requirements",
            "exact_address",
            "currency",
            "characteristics",
        ]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 5}),
            "requirements": forms.Textarea(attrs={"rows": 5}),
            "characteristics": forms.Textarea(attrs={"rows": 5}),
            "property_type": forms.Select(choices=Property.PROPERTY_TYPES),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["video_url"].required = False
        self.fields["requirements"].required = False
        self.fields["exact_address"].required = False
        self.fields["characteristics"].required = False
        self.fields["video"].required = False  # Video opcional

    def clean_video(self):
        video = self.cleaned_data.get("video")
        if video:
            # Verificar que el archivo sea un video (extensión básica)
            valid_extensions = [".mp4", ".avi", ".mov"]
            ext = "." + video.name.split(".")[-1].lower()
            if ext not in valid_extensions:
                raise forms.ValidationError(
                    "Solo se aceptan archivos de video con extensiones .mp4, .avi o .mov."
                )
            # Verificar duración (aproximación básica, se puede mejorar con bibliotecas como moviepy)
            # Nota: Esta validación es limitada sin procesar el archivo; se recomienda usar un backend para precisión
            max_duration_seconds = 180  # 3 minutos
            # Aquí solo verificamos el tamaño como aproximación (puedes mejorar esto)
            if video.size > 50 * 1024 * 1024:  # Límite aproximado de 50MB (ajustable)
                raise forms.ValidationError(
                    "El video no debe superar los 3 minutos o 50MB."
                )
        return video


class PropertyPhotoForm(forms.ModelForm):
    class Meta:
        model = PropertyPhoto
        fields = ["image"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["image"].required = False
