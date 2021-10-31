import json
from django.contrib.auth import get_user_model
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from django.urls import reverse

from .models import PublicMessage, PrivateChatRoom, PrivateMessage
from .constants import CMD_JOIN_ROOM, CMD_LEAVE_ROOM, CMD_SEND_MESSAGE



class PrivatChatRoomConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["chat_id"]
        self.room_group_name = f"chat_{self.room_name}"
        self.user = self.scope["user"]

        try:
            chat = await sync_to_async(PrivateChatRoom.objects.get, thread_sensitive=True)(pk=self.room_name)
            self.chat_room = chat
            self.room_name = chat.room_name
            self.room_group_name = f"chat_{self.room_name}"
        except PrivateChatRoom.DoesNotExist:
            await self.close()
        
        is_member = await sync_to_async(chat.check_user, thread_sensitive=True)(self.user)
        if not is_member:
            await self.close()

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name,
        )
        await self.accept()

        if not await sync_to_async(self.chat_room.is_connected, thread_sensitive=True)(self.user):
            await sync_to_async(self.chat_room.join, thread_sensitive=True)(self.user)

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "system_message",
                    "command": CMD_JOIN_ROOM,
                    "username": self.user.username,
                    "connected_users_count": await sync_to_async(len, thread_sensitive=True)(await sync_to_async(self.chat_room.connected_users.all, thread_sensitive=True)()),
                }
            )

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name,
        )

        if await sync_to_async(self.chat_room.is_connected, thread_sensitive=True)(self.user):
            await sync_to_async(self.chat_room.leave, thread_sensitive=True)(self.user)

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "system_message",
                    "command": CMD_LEAVE_ROOM,
                    "username": self.user.username,
                    "connected_users_count": await sync_to_async(len, thread_sensitive=True)(await sync_to_async(self.chat_room.connected_users.all, thread_sensitive=True)()),
                }
            )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"].strip()
        username = text_data_json["username"]

        if username != self.user.username:
            await self.disconnect(close_code=4003)
            return

        if message:
            db_message = PrivateMessage(content=message, author=self.user, chat_room=self.chat_room)
            await sync_to_async(db_message.save, thread_sensitive=True)()
        
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chatroom_message",
                "command": CMD_SEND_MESSAGE,
                "message": message,
                "username": username,
                "user_url": reverse("account:profile", kwargs={"user_id": self.user.pk}),
            }
        )

    async def chatroom_message(self, event):
        command = event["command"]
        message = event["message"]
        username = event["username"]
        user_url = event["user_url"]

        await self.send(json.dumps({
            "command": command,
            "message": message,
            "username": username,
            "user_url": user_url,
        }))

    async def system_message(self, event):
        command = event["command"]
        username = event["username"]
        connected_users_count = event["connected_users_count"]

        await self.send(json.dumps({
            "command": command,
            "username": username,
            "connected_users_count": connected_users_count,
        }))


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
        
