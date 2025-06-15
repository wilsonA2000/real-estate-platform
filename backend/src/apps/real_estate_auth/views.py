from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.views.generic import CreateView, TemplateView, FormView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseRedirect

from .forms import CustomUserCreationForm, CustomAuthenticationForm, InterviewCodeGenerationForm
from .models import CustomUser, InterviewCode


class CustomLoginView(LoginView):
    """
    Vista personalizada para el inicio de sesión.
    """
    form_class = CustomAuthenticationForm
    template_name = 'registration/login.html'
    
    def form_valid(self, form):
        """
        Verificar si el usuario está verificado antes de permitir el inicio de sesión.
        """
        user = form.get_user()
        
        # Si el usuario no está verificado, mostrar un mensaje y redirigir
        if not user.is_verified and not user.is_superuser:
            messages.warning(
                self.request,
                _("Tu cuenta aún no ha sido verificada por un administrador. "
                  "Por favor, espera a que tu cuenta sea verificada para acceder.")
            )
            return HttpResponseRedirect(self.get_success_url())
        
        return super().form_valid(form)


class RegisterView(CreateView):
    """
    Vista para el registro de nuevos usuarios con validación de código de entrevista.
    """
    form_class = CustomUserCreationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(
            self.request,
            _("Tu cuenta ha sido creada exitosamente. Un administrador verificará tu cuenta pronto.")
        )
        return response


class AdminDashboardView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    """
    Panel de administración para superusuarios.
    """
    template_name = 'admin/dashboard.html'
    
    def test_func(self):
        return self.request.user.is_superuser
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Estadísticas de usuarios
        context['total_users'] = CustomUser.objects.count()
        context['verified_users'] = CustomUser.objects.filter(is_verified=True).count()
        context['unverified_users'] = CustomUser.objects.filter(is_verified=False).count()
        
        # Estadísticas por tipo de perfil
        context['arrendadores'] = CustomUser.objects.filter(profile_type='arrendador').count()
        context['arrendatarios'] = CustomUser.objects.filter(profile_type='arrendatario').count()
        context['prestadores'] = CustomUser.objects.filter(profile_type='prestador').count()
        
        # Estadísticas de códigos de entrevista
        context['total_codes'] = InterviewCode.objects.count()
        context['used_codes'] = InterviewCode.objects.filter(is_used=True).count()
        context['available_codes'] = InterviewCode.objects.filter(is_used=False).count()
        
        # Usuarios recientes
        context['recent_users'] = CustomUser.objects.order_by('-date_joined')[:10]
        
        return context


class GenerateInterviewCodesView(LoginRequiredMixin, UserPassesTestMixin, FormView):
    """
    Vista para generar códigos de entrevista en lote.
    """
    template_name = 'admin/generate_codes.html'
    form_class = InterviewCodeGenerationForm
    success_url = reverse_lazy('generate_codes')
    
    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff
    
    def form_valid(self, form):
        profile_type = form.cleaned_data['profile_type']
        quantity = form.cleaned_data['quantity']
        rating = form.cleaned_data['rating']
        notes = form.cleaned_data['notes']
        
        generated_codes = []
        for _ in range(quantity):
            code = InterviewCode.generate_code()
            interview_code = InterviewCode.objects.create(
                code=code,
                profile_type=profile_type,
                rating=rating,
                notes=notes,
                created_by=self.request.user
            )
            generated_codes.append(interview_code)
        
        messages.success(
            self.request,
            _("Se han generado {} códigos de entrevista para {}.").format(
                quantity, dict(InterviewCode.PROFILE_CHOICES)[profile_type]
            )
        )
        
        # Pasar los códigos generados al contexto
        self.extra_context = {'generated_codes': generated_codes}
        
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Mostrar los códigos disponibles más recientes
        context['available_codes'] = InterviewCode.objects.filter(
            is_used=False
        ).order_by('-created_at')[:10]
        return context


@login_required
@user_passes_test(lambda u: u.is_superuser)
def verify_user(request, user_id):
    """
    Verificar un usuario específico.
    """
    try:
        user = CustomUser.objects.get(id=user_id)
        user.is_verified = True
        user.verification_date = timezone.now()
        user.verified_by = request.user
        user.save()
        
        messages.success(request, _(f"El usuario {user.username} ha sido verificado."))
    except CustomUser.DoesNotExist:
        messages.error(request, _("Usuario no encontrado."))
    
    return redirect('admin_dashboard')