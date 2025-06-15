# real_estate/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from apps.properties.views import (
    PropertyListView,
    PropertyDetailView,
    PropertyCreateView,
    PropertyUpdateView,
    PropertyDeleteView,
)

urlpatterns = [
    # Admin de Django
    path("admin/", admin.site.urls),
    
    # Autenticación y gestión de usuarios
    path("", include("apps.real_estate_auth.urls")),
    
    # Páginas estáticas
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
    
    # Propiedades
    path("property-list/", PropertyListView.as_view(), name="property_list"),
    path("property/<int:pk>/", PropertyDetailView.as_view(), name="property_detail"),
    path("property/create/", PropertyCreateView.as_view(), name="property_create"),
    path("property/<int:pk>/edit/", PropertyUpdateView.as_view(), name="property_edit"),
    path("property/<int:pk>/delete/", PropertyDeleteView.as_view(), name="property_delete"),
    
    # Aplicaciones
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
    path("contact-requests/", include("apps.contact.urls")),
]

# Sirve archivos de media y estáticos en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)