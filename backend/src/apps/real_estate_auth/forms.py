from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.utils.translation import gettext_lazy as _
from .models import CustomUser, InterviewCode


class CustomUserCreationForm(UserCreationForm):
    """
    Formulario personalizado para la creación de usuarios que incluye
    la validación del código de entrevista.
    """
    interview_code = forms.CharField(
        label=_("Código de entrevista"),
        max_length=10,
        required=True,
        help_text=_("Ingrese el código de entrevista proporcionado por VeriHome."),
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: ABC123XY'})
    )

    class Meta:
        model = CustomUser
        fields = ('username', 'name', 'email', 'profile_type', 'interview_code', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de usuario'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre completo'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'correo@ejemplo.com'}),
            'profile_type': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean_interview_code(self):
        """
        Valida que el código de entrevista exista, no esté usado y corresponda al tipo de perfil.
        """
        code = self.cleaned_data.get('interview_code')
        profile_type = self.cleaned_data.get('profile_type')
        
        if not code:
            raise forms.ValidationError(_("Debe ingresar un código de entrevista."))
        
        try:
            interview_code = InterviewCode.objects.get(code=code)
        except InterviewCode.DoesNotExist:
            raise forms.ValidationError(_("El código de entrevista no es válido."))
        
        if interview_code.is_used:
            raise forms.ValidationError(_("Este código de entrevista ya ha sido utilizado."))
        
        if interview_code.profile_type != profile_type:
            raise forms.ValidationError(_("El código de entrevista no corresponde al tipo de perfil seleccionado."))
        
        return code

    def save(self, commit=True):
        user = super().save(commit=False)
        
        # Obtener el código de entrevista y asignar la calificación inicial
        code = self.cleaned_data.get('interview_code')
        interview_code = InterviewCode.objects.get(code=code)
        user.rating = interview_code.rating
        
        if commit:
            user.save()
            # Marcar el código como utilizado
            interview_code.is_used = True
            interview_code.save()
        
        return user


class CustomAuthenticationForm(AuthenticationForm):
    """
    Formulario personalizado para la autenticación de usuarios.
    """
    username = forms.CharField(
        label=_("Usuario"),
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de usuario'})
    )
    password = forms.CharField(
        label=_("Contraseña"),
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña'})
    )


class InterviewCodeGenerationForm(forms.Form):
    """
    Formulario para generar códigos de entrevista en lote.
    """
    PROFILE_CHOICES = (
        ("arrendador", "Arrendador"),
        ("arrendatario", "Arrendatario"),
        ("prestador", "Prestador de Servicios"),
    )
    
    profile_type = forms.ChoiceField(
        label=_("Tipo de perfil"),
        choices=PROFILE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    quantity = forms.IntegerField(
        label=_("Cantidad"),
        min_value=1,
        max_value=100,
        initial=5,
        help_text=_("Número de códigos a generar (máximo 100)"),
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    
    rating = forms.IntegerField(
        label=_("Calificación inicial"),
        min_value=1,
        max_value=5,
        initial=3,
        help_text=_("Calificación inicial para los usuarios que usen estos códigos (1-5)"),
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    
    notes = forms.CharField(
        label=_("Notas"),
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Notas adicionales sobre estos códigos'})
    )