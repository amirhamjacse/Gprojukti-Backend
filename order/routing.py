from django.urls import re_path
from .consumers import OrderNotificationConsumer

websocket_urlpatterns = [
    re_path(r'ws/order_notifications/$', OrderNotificationConsumer.as_asgi()),
]