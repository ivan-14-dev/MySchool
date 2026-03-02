# backend/apps/communication/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model

User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        if self.user.is_anonymous:
            await self.close()
            return

        self.room_name = f"user_{self.user.id}"
        self.room_group_name = f"chat_{self.room_name}"

        # Rejoindre le groupe de room
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Quitter le groupe de room
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        message_type = text_data_json.get("type", "chat_message")

        # Envoyer le message au groupe
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": message_type,
                "message": message,
                "user_id": str(self.user.id),
            }
        )

    async def chat_message(self, event):
        # Envoyer le message au WebSocket
        await self.send(text_data=json.dumps({
            "message": event["message"],
            "user_id": event["user_id"],
            "type": "chat_message"
        }))

    async def notification(self, event):
        # Envoyer une notification au WebSocket
        await self.send(text_data=json.dumps({
            "type": "notification",
            "title": event["title"],
            "message": event["message"],
            "notification_type": event.get("notification_type", "info")
        }))