from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

websocket_urlpatterns = ProtocolTypeRouter({
    "websocket":AuthMiddlewareStack(
        URLRouter(
            []
        )
    )
})