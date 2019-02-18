from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import like_action.routing

application = ProtocolTypeRouter({
    #http -> django views is added by default
    'websocket': AuthMiddlewareStack(
        URLRouter(
            like_action.routing.websocket_urlpatterns
        )
    )
})