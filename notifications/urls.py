from django.urls import re_path
from AtruX import consumers

websocket_urlpatterns = [
    re_path(r'ws/notifications-server/', consumers.NotificationsConsumer.as_asgi())
]
