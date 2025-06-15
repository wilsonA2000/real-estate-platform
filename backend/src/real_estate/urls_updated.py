# real_estate/urls.py
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from apps.real_estate_auth.views import CustomLoginView, RegisterView
from apps.properties.views import (
    PropertyListView,
    PropertyDetailView,
    PropertyCreateView,
    PropertyUpdateView,
)
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

urlpatterns = [
    # Admin
    path("admin/", admin.site.urls),
    # Auth
    path("login/", CustomLoginView.as_view(), name="login"),
    path("register/", RegisterView.as_view(), name="register"),
    path("logout/", auth_views.LogoutView.as_view(next_page="home"), name="logout"),
    # Password Reset
    path(
        "password-reset/",
        auth_views.PasswordResetView.as_view(
            template_name="registration/password_reset.html",
            email_template_name="registration/password_reset_email.html",
            subject_template_name="registration/password_reset_subject.txt",
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
    # Pages
    path("", TemplateView.as_view(template_name="home.html"), name="home"),
    path(
        "contact/", TemplateView.as_view(template_name="contact.html"), name="contact"
    ),
    path(
        "how-it-works/",
        TemplateView.as_view(template_name="how_it_works.html"),
        name="how_it_works",
    ),
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
    # Properties
    path("property-list/", PropertyListView.as_view(), name="property_list"),
    path("property/<int:pk>/", PropertyDetailView.as_view(), name="property_detail"),
    path("property/create/", PropertyCreateView.as_view(), name="property_create"),
    path("property/<int:pk>/edit/", PropertyUpdateView.as_view(), name="property_edit"),
    # Applications
    path("ratings/", include("apps.ratings.urls")),
    path("messaging/", include("apps.messaging.urls")),
    path("community/", include("apps.community.urls")),
    path("contracts/", include("apps.contracts.urls")),
    path("payments/", include("apps.payments.urls")),
    path("ai/", include("ai.urls")),
    path("webhooks/", include("webhooks.urls")),
    path("documents/", include("apps.documents.urls")),
    path("resume/", include("apps.resume.urls")),
    path("news/", include("apps.news.urls")),
    
    # API Documentation
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("api/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
]

# Sirve archivos de media y estáticos en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)