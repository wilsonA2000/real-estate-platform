import time
from django.http import HttpResponse
from django.core.cache import cache

class RateLimitMiddleware:
    """
    Middleware para limitar la tasa de solicitudes por IP.
    """
    def __init__(self, get_response):
        self.get_response = get_response
        # Configuración: solicitudes máximas por minuto
        self.rate_limit = 60  # 60 solicitudes por minuto
        self.time_frame = 60  # 60 segundos (1 minuto)

    def __call__(self, request):
        # Excluir rutas específicas (como archivos estáticos)
        if request.path.startswith('/static/') or request.path.startswith('/media/'):
            return self.get_response(request)

        # Obtener la IP del cliente
        ip = self.get_client_ip(request)
        
        # Clave única para esta IP en el cache
        cache_key = f"rate_limit_{ip}"
        
        # Obtener el historial de solicitudes para esta IP
        request_history = cache.get(cache_key, [])
        
        # Limpiar el historial (eliminar solicitudes antiguas)
        current_time = time.time()
        request_history = [timestamp for timestamp in request_history 
                          if current_time - timestamp < self.time_frame]
        
        # Verificar si se excede el límite
        if len(request_history) >= self.rate_limit:
            return HttpResponse(
                "Demasiadas solicitudes. Por favor, inténtelo de nuevo más tarde.",
                status=429
            )
        
        # Añadir la solicitud actual al historial
        request_history.append(current_time)
        
        # Actualizar el cache
        cache.set(cache_key, request_history, self.time_frame)
        
        # Procesar la solicitud normalmente
        return self.get_response(request)
    
    def get_client_ip(self, request):
        """Obtiene la dirección IP del cliente."""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip