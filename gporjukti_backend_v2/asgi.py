import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator
import order.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gporjukti_backend_v2.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(
                order.routing.websocket_urlpatterns
            )
        )
    ),
})
