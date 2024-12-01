import json
from channels.generic.websocket import AsyncWebsocketConsumer 
from channels.db import database_sync_to_async
from .models import Room, Message

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        # Join room group 
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        anonymous_name = text_data_json['anonymous_name']

        await self.save_message(anonymous_name, message)
        
        await self.channel_layer.grouo_send(
            self.room_group_name,
            {
                "type" : "chat message",
                'message' : message,
                'anonymous_name' : anonymous_name
            }
        )
        async def chat_message(self, event):
            message = event['message']
            anonymous_name = event['anonymous_name']

            await self.send(text_data=json.dumps({
                'message' : message,
                'anonymous_name' : anonymous_name
            }))

        @database_sync_to_async
        def save_message(self, anonymous_name, message):
            room = Room.objects.get(name=self.room_name)
            Message.objects.create(
                room=room,
                content=message,
                anonymous_name=anonymous_name
            )

