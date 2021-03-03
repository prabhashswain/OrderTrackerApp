import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter,URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import path
from home.consumers import PizzaConsumer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'OrderTrackerProj.settings')

application = get_asgi_application()

ws_pattern = [
    path('ws/pizza/<order_id>',PizzaConsumer.as_asgi())
]

application = ProtocolTypeRouter({
    "websocket":AuthMiddlewareStack(
        URLRouter(
            ws_pattern
        )
    )
})