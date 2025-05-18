from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LoginView
from django.views import View
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from .models import CustomUser  # Import CustomUser from the models module


class CustomLoginView(LoginView):
    form_class = CustomAuthenticationForm
    template_name = "registration/login.html"
    redirect_authenticated_user = True

    def form_valid(self, form):
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=username, password=password)

        if user is not None:
            login(self.request, user)
            messages.success(self.request, _("¡Bienvenido de nuevo!"))
            # Redirección según perfil
            if user.profile_type == "prestador":
                return redirect("/")  # Redirige a la página principal para prestadores
            else:
                next_url = self.request.POST.get("next", "/property-list/")
                return redirect(next_url)
        return super().form_invalid(form)


class RegisterView(View):
    template_name = "registration/register.html"
    success_url = "/"

    def get(self, request):
        if request.user.is_authenticated:
            return redirect(self.success_url)
        form = CustomUserCreationForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(
                request, _("¡Registro exitoso! Bienvenido a la plataforma.")
            )
            # Redirección basada en el perfil del usuario
            if user.profile_type == "arrendador":
                return redirect("/property-list/")
            elif user.profile_type == "arrendatario":
                return redirect("/property-list/")
            elif user.profile_type == "prestador":
                return redirect("/")  # Redirige a la página principal para prestadores
            return redirect(self.success_url)

        # Manejo detallado de errores
        if not form.is_valid():
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{form.fields[field].label}: {error}")
            return render(
                request,
                self.template_name,
                {"form": form, "profile_choices": dict(CustomUser.PROFILE_CHOICES)},
            )

        return render(
            request,
            self.template_name,
            {"form": form, "profile_choices": dict(CustomUser.PROFILE_CHOICES)},
        )
