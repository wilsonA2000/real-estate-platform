from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import CustomUser
from .forms import CustomUserCreationForm, CustomUserChangeForm


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser

    list_display = (
        "email",
        "name",
        "get_profile_type_display",
        "phone_number",
        "is_active",
        "is_staff",
    )
    list_filter = ("profile_type", "is_staff", "is_active", "date_joined")
    search_fields = ("email", "name", "username", "phone_number")
    ordering = ("-date_joined",)
    readonly_fields = ("last_login", "date_joined")

    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (
            _("Información Personal"),
            {
                "fields": (
                    "name",
                    "email",
                    "profile_type",
                    "phone_number",
                    "profile_picture",
                )
            },
        ),
        (
            _("Permisos"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (
            _("Fechas Importantes"),
            {"fields": ("last_login", "date_joined"), "classes": ("collapse",)},
        ),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "email",
                    "name",
                    "profile_type",
                    "phone_number",
                    "password1",
                    "password2",
                    "is_active",
                    "is_staff",
                ),
            },
        ),
    )

    filter_horizontal = (
        "groups",
        "user_permissions",
    )


admin.site.register(CustomUser, CustomUserAdmin)
