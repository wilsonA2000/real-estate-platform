# Instrucciones para aplicar las mejoras

Este documento contiene las instrucciones para aplicar todas las mejoras sugeridas al proyecto.

## 1. Configuración de Base de Datos PostgreSQL

Para cambiar de SQLite a PostgreSQL:

1. Asegúrate de tener PostgreSQL instalado y funcionando
2. Crea una base de datos llamada `real_estate`
3. Actualiza el archivo `.env` con las credenciales de PostgreSQL:
   ```
   DB_NAME=real_estate
   DB_USER=tu_usuario
   DB_PASSWORD=tu_contraseña
   DB_HOST=localhost
   DB_PORT=5432
   ```
4. Reemplaza el archivo `settings.py` con el nuevo archivo `settings_updated.py`
5. Ejecuta las migraciones:
   ```
   python manage.py migrate
   ```

## 2. Documentación de API

La documentación de API ya está configurada con drf-spectacular. Para activarla:

1. Reemplaza el archivo `urls.py` con el nuevo archivo `urls_updated.py`
2. Asegúrate de que drf-spectacular esté instalado:
   ```
   pip install drf-spectacular
   ```
3. Accede a la documentación en:
   - `/api/docs/` para Swagger UI
   - `/api/redoc/` para ReDoc

## 3. Tests Unitarios

Se han creado tests unitarios para los modelos y vistas principales:

1. Para ejecutar los tests:
   ```
   python manage.py test
   ```

## 4. Optimización de Consultas

Se han añadido índices a campos frecuentemente consultados como `property_type`.

## 5. Seguridad Adicional

Se ha implementado un middleware de rate limiting para proteger contra ataques de fuerza bruta:

1. Asegúrate de que el middleware esté incluido en la configuración de MIDDLEWARE en settings.py

## 6. Gestión de Dependencias

Se han creado archivos separados para dependencias de desarrollo:

1. Para instalar las dependencias de desarrollo:
   ```
   pip install -r requirements-dev.txt
   ```

## 7. Despliegue con Docker

Se ha configurado Docker para facilitar el despliegue:

1. Para construir y ejecutar los contenedores:
   ```
   docker-compose up -d
   ```

## 8. API RESTful

Se han creado vistas de API para propiedades:

1. Importa las nuevas URLs de API en el archivo principal de URLs:
   ```python
   path('api/', include('apps.properties.api_urls')),
   ```

## 9. Logging Mejorado

Se ha configurado un sistema de logging más robusto en el archivo `settings_updated.py`.

## 10. Variables de Entorno

Se ha creado un archivo `.env.example` con todas las variables de entorno necesarias.

## Nota Final

Después de aplicar todas estas mejoras, tu aplicación será más robusta, escalable y mantenible. Asegúrate de probar cada cambio antes de implementarlo en producción.