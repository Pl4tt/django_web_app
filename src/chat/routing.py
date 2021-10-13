from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r"ws/chat/public/$", consumers.PublicChatRoomConsumer.as_asgi()),
    re_path(r"ws/chat/private/(?P<chat_id>\w+)/$", consumers.PrivatChatRoomConsumer.as_asgi()),
]