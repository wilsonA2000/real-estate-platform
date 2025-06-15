from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.contrib import messages
from django.urls import reverse
from django.utils.html import format_html
from .models import CustomUser, Contract, InterviewCode


class InterviewCodeAdmin(admin.ModelAdmin):
    list_display = ('code', 'profile_type', 'rating', 'is_used', 'created_at', 'created_by')
    list_filter = ('profile_type', 'is_used', 'rating', 'created_at')
    search_fields = ('code', 'notes')
    readonly_fields = ('created_at',)
    fieldsets = (
        (None, {'fields': ('code', 'profile_type', 'rating', 'is_used')}),
        (_('Información adicional'), {'fields': ('notes', 'created_at', 'created_by')}),
    )
    actions = ['generate_new_codes']

    def save_model(self, request, obj, form, change):
        if not obj.pk:  # Si es un nuevo objeto
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

    def generate_new_codes(self, request, queryset):
        """
        Acción para generar nuevos códigos de entrevista.
        """
        count = 0
        for profile_type, _ in InterviewCode.PROFILE_CHOICES:
            for _ in range(5):  # Generar 5 códigos por tipo de perfil
                code = InterviewCode.generate_code()
                InterviewCode.objects.create(
                    code=code,
                    profile_type=profile_type,
                    created_by=request.user
                )
                count += 1
        
        messages.success(request, f'Se han generado {count} nuevos códigos de entrevista.')
    
    generate_new_codes.short_description = _("Generar nuevos códigos de entrevista")


class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'name', 'email', 'profile_type', 'is_verified', 'rating', 'date_joined')
    list_filter = ('profile_type', 'is_verified', 'is_staff', 'is_active', 'date_joined')
    search_fields = ('username', 'name', 'email', 'interview_code')
    readonly_fields = ('date_joined', 'last_login', 'verification_date', 'verified_by')
    actions = ['verify_users', 'unverify_users']
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Información personal'), {'fields': ('name', 'email', 'phone_number', 'profile_picture')}),
        (_('Perfil'), {'fields': ('profile_type', 'interview_code', 'rating', 'resume')}),
        (_('Verificación'), {'fields': ('is_verified', 'verification_date', 'verified_by')}),
        (_('Permisos'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Fechas importantes'), {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'name', 'email', 'profile_type', 'interview_code'),
        }),
    )
    
    def verify_users(self, request, queryset):
        """
        Acción para verificar usuarios seleccionados.
        """
        updated = queryset.update(is_verified=True, verification_date=timezone.now(), verified_by=request.user)
        messages.success(request, f'Se han verificado {updated} usuarios.')
    
    verify_users.short_description = _("Marcar usuarios como verificados")
    
    def unverify_users(self, request, queryset):
        """
        Acción para quitar la verificación de usuarios seleccionados.
        """
        updated = queryset.update(is_verified=False, verification_date=None, verified_by=None)
        messages.success(request, f'Se ha quitado la verificación a {updated} usuarios.')
    
    unverify_users.short_description = _("Quitar verificación de usuarios")


class ContractAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_parties', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('id', 'parties__username', 'parties__name')
    
    def get_parties(self, obj):
        return ", ".join([str(party) for party in obj.parties.all()])
    
    get_parties.short_description = _("Partes involucradas")


# Registrar los modelos en el admin
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Contract, ContractAdmin)
admin.site.register(InterviewCode, InterviewCodeAdmin)