from django.urls import re_path
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path

from . import consumers

# websocket_urlpatterns = [
#     # re_path(r'ws/booksharingapi/web_socket/$', consumers.ChatConsumer),
#     re_path(r'ws/chat/(?P<room_name>\w+)/$', consumers.NotificationConsumer),
# ]

websockets = URLRouter([
    path(
        "ws/notifications/",
        consumers.NotificationConsumer,
        name="ws_notifications",
    ),
])