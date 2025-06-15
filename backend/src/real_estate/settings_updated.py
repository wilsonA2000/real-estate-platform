import os
from pathlib import Path
from django.core.exceptions import ImproperlyConfigured
from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = (
    Path(__file__).resolve().parent.parent.parent
)  # Ajustado para src/real_estate

# ====================== SECURITY SETTINGS ======================
SECRET_KEY = config("SECRET_KEY")
DEBUG = config("DEBUG", default=True, cast=bool)

ALLOWED_HOSTS = ["localhost", "127.0.0.1"]
CSRF_TRUSTED_ORIGINS = ["http://localhost:8000", "http://127.0.0.1:8000"]

# ====================== APPLICATION DEFINITION ======================
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "apps.real_estate_auth.apps.RealEstateAuthConfig",
    "apps.properties.apps.PropertiesConfig",
    "apps.ratings.apps.RatingsConfig",
    "apps.messaging.apps.MessagingConfig",
    # Third-party apps
    "rest_framework",
    "corsheaders",
    "channels",
    "widget_tweaks",
    "drf_spectacular",
    # Local apps
    "real_estate",
    "apps.community.apps.CommunityConfig",
    "apps.contracts.apps.ContractsConfig",
    "apps.payments.apps.PaymentsConfig",
    "apps.documents.apps.DocumentsConfig",
    "apps.resume.apps.ResumeConfig",
    "apps.news.apps.NewsConfig",
    "apps.contact.apps.ContactConfig",
    "apps.notifications.apps.NotificationsConfig",  # Sistema de notificaciones
    "real_estate_channels",
    "ai",
    "webhooks",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "middleware.ratelimit_middleware.RateLimitMiddleware",
]

ROOT_URLCONF = "real_estate.urls"
WSGI_APPLICATION = "real_estate.wsgi.application"
ASGI_APPLICATION = "real_estate.asgi.application"

# ====================== TEMPLATES ======================
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.media",
                "django.template.context_processors.csrf",
            ],
            "builtins": ["widget_tweaks.templatetags.widget_tweaks"],
        },
    },
]

# ====================== DATABASE ======================
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": config("DB_NAME", default="real_estate"),
        "USER": config("DB_USER", default="user"),
        "PASSWORD": config("DB_PASSWORD", default="password"),
        "HOST": config("DB_HOST", default="localhost"),
        "PORT": config("DB_PORT", default="5432"),
    }
}

# ====================== AUTHENTICATION ======================
AUTH_USER_MODEL = "real_estate_auth.CustomUser"

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
        "OPTIONS": {"user_attributes": ("username", "email", "name")},
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        "OPTIONS": {
            "min_length": 8,
        },
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

LOGIN_URL = "/login/"
LOGIN_REDIRECT_URL = "/property-list/"
LOGOUT_REDIRECT_URL = "/"

# ====================== INTERNATIONALIZATION ======================
LANGUAGE_CODE = "es-co"
TIME_ZONE = "America/Bogota"
USE_I18N = True
USE_L10N = True
USE_TZ = True

# ====================== STATIC & MEDIA FILES ======================
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"
# Añadimos STATICFILES_STORAGE para producción
if not DEBUG:
    STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
else:
    STATICFILES_STORAGE = "django.contrib.staticfiles.storage.ManifestStaticFilesStorage"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# Aumentamos el límite de tamaño para videos (50MB)
FILE_UPLOAD_MAX_MEMORY_SIZE = 52428800  # 50MB en bytes

# ====================== GOOGLE MAPS API KEY ======================
GOOGLE_MAPS_API_KEY = config("GOOGLE_MAPS_API_KEY", default="")

# ====================== EMAIL CONFIGURATION ======================
if DEBUG:
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
else:
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
    EMAIL_HOST = config("EMAIL_HOST", default="smtp.gmail.com")
    EMAIL_PORT = config("EMAIL_PORT", default=587, cast=int)
    EMAIL_USE_TLS = config("EMAIL_USE_TLS", default=True, cast=bool)
    EMAIL_HOST_USER = config("EMAIL_HOST_USER")
    EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD")

DEFAULT_FROM_EMAIL = config(
    "DEFAULT_FROM_EMAIL", default="no-reply@realestateplatform.com"
)

# ====================== SECURITY HEADERS ======================
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
else:
    SECURE_SSL_REDIRECT = False

SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"

# ====================== CORS SETTINGS ======================
CORS_ALLOW_ALL_ORIGINS = DEBUG
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

# ====================== CHANNELS ======================
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [(config("REDIS_HOST", default="127.0.0.1"), config("REDIS_PORT", default=6379, cast=int))],
        },
    },
}

# ====================== REST FRAMEWORK ======================
REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
    ],
}

# ====================== DRF SPECTACULAR ======================
SPECTACULAR_SETTINGS = {
    'TITLE': 'API de Plataforma Inmobiliaria',
    'DESCRIPTION': 'API para gestionar propiedades, usuarios, mensajes y contratos',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
}

# ====================== CUSTOM SETTINGS ======================
PASSWORD_RESET_TIMEOUT = 172800

SESSION_COOKIE_AGE = 1209600
SESSION_SAVE_EVERY_REQUEST = True

FILE_UPLOAD_PERMISSIONS = 0o644

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {process:d} {thread:d} {message}",
            "style": "{",
        },
        "simple": {
            "format": "{levelname} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
        "file": {
            "class": "logging.FileHandler",
            "filename": BASE_DIR / "logs/django.log",
            "formatter": "verbose",
        },
    },
    "root": {
        "handlers": ["console", "file"],
        "level": "INFO",
    },
    "loggers": {
        "django": {
            "handlers": ["console", "file"],
            "level": "INFO",
            "propagate": False,
        },
    },
}