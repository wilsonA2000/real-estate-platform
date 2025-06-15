"""
ASGI config for real_estate project.
"""

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import real_estate_channels.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'real_estate.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            real_estate_channels.routing.websocket_urlpatterns
        )
    ),
})