from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views
from apps.properties.views import (
    PropertyListView,
    PropertyDetailView,
    PropertyCreateView,
)
from apps.real_estate_auth.views import CustomLoginView, RegisterView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", TemplateView.as_view(template_name="home.html"), name="home"),
    path(
        "contact/", TemplateView.as_view(template_name="contact.html"), name="contact"
    ),
    path(
        "how-it-works/",
        TemplateView.as_view(template_name="how_it_works.html"),
        name="how_it_works",
    ),
    path("login/", CustomLoginView.as_view(), name="login"),
    path("register/", RegisterView.as_view(), name="register"),
    path(
        "about-us/",
        TemplateView.as_view(template_name="about_us.html"),
        name="about_us",
    ),
    path(
        "privacy-policy/",
        TemplateView.as_view(template_name="privacy_policy.html"),
        name="privacy_policy",
    ),
    path("property-list/", PropertyListView.as_view(), name="property_list"),
    path("property/<int:pk>/", PropertyDetailView.as_view(), name="property_detail"),
    path("property/create/", PropertyCreateView.as_view(), name="property_create"),
    path("logout/", auth_views.LogoutView.as_view(next_page="home"), name="logout"),
    # URLs para password reset (opcional pero recomendado)
    path(
        "password-reset/",
        auth_views.PasswordResetView.as_view(
            template_name="registration/password_reset.html"
        ),
        name="password_reset",
    ),
    path(
        "password-reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="registration/password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "password-reset-confirm/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="registration/password_reset_confirm.html"
        ),
        name="password_reset_confirm",
    ),
    path(
        "password-reset-complete/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="registration/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
