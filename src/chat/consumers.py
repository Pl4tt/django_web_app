import json
from django.contrib.auth import get_user_model
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async

from .models import PublicMessage


class PublicChatRoomConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = "public"
        self.room_group_name = "chat_public"

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"].strip()
        username = text_data_json["username"]

        try:
            user = await sync_to_async(get_user_model().objects.get, thread_sensitive=True)(username=username)
        except get_user_model().DoesNotExist:
            await self.disconnect(close_code=4003)
            return

        if message:
            db_message = PublicMessage(content=message, author=user)
            await sync_to_async(db_message.save, thread_sensitive=True)()

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chatroom_message",
                "message": message,
                "username": username,
            }
        )
    
    async def chatroom_message(self, event):
        message = event["message"]
        username = event["username"]

        await self.send(text_data=json.dumps({
            "message": message,
            "username": username,
        }))
        
