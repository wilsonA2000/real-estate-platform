from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from django.urls import path

urlpatterns = [
    # Endpoints para la documentación de la API
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]

# Configuración para drf-spectacular
SPECTACULAR_SETTINGS = {
    'TITLE': 'API de Plataforma Inmobiliaria',
    'DESCRIPTION': 'API para gestionar propiedades, usuarios, mensajes y contratos',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    'COMPONENT_SPLIT_REQUEST': True,
    'SCHEMA_PATH_PREFIX': '/api/',
    'TAGS': [
        {'name': 'auth', 'description': 'Operaciones de autenticación'},
        {'name': 'properties', 'description': 'Operaciones con propiedades'},
        {'name': 'messaging', 'description': 'Sistema de mensajería'},
        {'name': 'contracts', 'description': 'Gestión de contratos'},
        {'name': 'payments', 'description': 'Procesamiento de pagos'},
    ],
}