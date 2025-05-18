from django import forms
from django.contrib.auth.forms import (
    UserCreationForm,
    UserChangeForm,
    AuthenticationForm,
)
from django.utils.translation import gettext_lazy as _
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        label=_("Correo Electrónico"),
        required=True,
        widget=forms.EmailInput(attrs={"autocomplete": "email"}),
    )
    phone_number = forms.CharField(
        label=_("Teléfono"),
        required=False,
        widget=forms.TextInput(attrs={"placeholder": _("Opcional")}),
    )

    class Meta:
        model = CustomUser
        fields = (
            "username",
            "email",
            "name",
            "profile_type",
            "phone_number",
            "password1",
            "password2",
        )
        labels = {
            "profile_type": _("Tipo de Perfil"),
        }
        widgets = {
            "profile_type": forms.Select(attrs={"class": "form-select"}),
        }

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError(_("Este correo ya está registrado."))
        return email


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = "__all__"
        widgets = {
            "profile_type": forms.Select(attrs={"class": "form-select"}),
        }


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        label=_("Usuario o Correo"),
        widget=forms.TextInput(
            attrs={"autofocus": True, "placeholder": _("Usuario o correo electrónico")}
        ),
    )
    error_messages = {
        "invalid_login": _(
            "Por favor ingrese un %(username)s y contraseña correctos. "
            "Note que ambos campos pueden ser sensibles a mayúsculas."
        ),
        "inactive": _("Esta cuenta está inactiva."),
    }
