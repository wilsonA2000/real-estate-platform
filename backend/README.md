# Plataforma Inmobiliaria - Backend

Backend para una plataforma inmobiliaria desarrollada con Django y Django REST Framework.

## Características

- Gestión de propiedades inmobiliarias
- Sistema de autenticación personalizado
- Mensajería entre usuarios
- Contratos digitales
- Procesamiento de pagos
- Integración con IA para chatbot y análisis de imágenes
- WebSockets para comunicación en tiempo real

## Requisitos

- Python 3.9+
- PostgreSQL
- Redis (para WebSockets)

## Instalación

1. Clonar el repositorio:
```bash
git clone <url-del-repositorio>
cd real-estate-platform/backend
```

2. Crear un entorno virtual:
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

4. Configurar variables de entorno:
```bash
cp .env.example .env
# Editar .env con tus configuraciones
```

5. Ejecutar migraciones:
```bash
python manage.py migrate
```

6. Crear superusuario:
```bash
python manage.py createsuperuser
```

7. Iniciar el servidor:
```bash
python manage.py runserver
```

## Estructura del Proyecto

```
backend/
├── media/                # Archivos subidos por usuarios
├── src/                  # Código fuente principal
│   ├── ai/               # Módulos de inteligencia artificial
│   ├── apps/             # Aplicaciones Django
│   │   ├── community/    # Gestión de comunidad
│   │   ├── contact/      # Formularios de contacto
│   │   ├── contracts/    # Gestión de contratos
│   │   ├── documents/    # Gestión de documentos
│   │   ├── messaging/    # Sistema de mensajería
│   │   ├── news/         # Noticias y blog
│   │   ├── payments/     # Procesamiento de pagos
│   │   ├── properties/   # Gestión de propiedades
│   │   ├── ratings/      # Sistema de calificaciones
│   │   ├── real_estate_auth/ # Autenticación personalizada
│   │   └── resume/       # Hojas de vida
│   ├── logger/           # Configuración de logging
│   ├── middleware/       # Middlewares personalizados
│   ├── real_estate/      # Configuración principal
│   ├── real_estate_channels/ # Configuración de WebSockets
│   ├── services/         # Servicios compartidos
│   └── webhooks/         # Webhooks para integraciones
├── static/               # Archivos estáticos
├── templates/            # Plantillas HTML
├── .env                  # Variables de entorno
├── .env.example          # Ejemplo de variables de entorno
├── docker-compose.yml    # Configuración de Docker
├── Dockerfile            # Configuración para contenedor
├── manage.py             # Script de gestión de Django
└── requirements.txt      # Dependencias del proyecto
```

## Documentación de API

La documentación de la API está disponible en:

- Swagger UI: `/api/docs/`
- ReDoc: `/api/redoc/`
- Schema (OpenAPI): `/api/schema/`

## Desarrollo

Para desarrollo, instala las dependencias adicionales:

```bash
pip install -r requirements-dev.txt
```

### Ejecutar pruebas

```bash
pytest
```

### Verificar cobertura de código

```bash
coverage run -m pytest
coverage report
```

## Despliegue con Docker

```bash
docker-compose up -d
```

## Licencia

Este proyecto es privado y no está disponible para uso público.