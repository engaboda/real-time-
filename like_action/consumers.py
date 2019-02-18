from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

from django.contrib.auth.models import User

import json

class LikeAddConsumer(AsyncWebsocketConsumer):
    '''
    '''
    async def connect(self):
        self.room_name = 'plus'
        self.room_group_name = 'channel_{}'.format(self.room_name)

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
        plus = text_data_json.get('add_one')
        minus = text_data_json.get('minus_one')
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type':'like',
                'message': plus if plus else minus
            }
        )        

    async def like(self, event):
        message = event['message']
        await self.send(text_data=json.dumps({
            'message':message,
        }))

class CountUserConsumer(AsyncWebsocketConsumer):
    '''
    '''
    async def connect(self):
        self.room_name = 'count_user'
        self.room_group_name = 'channels_{}'.format(self.room_name)
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
        self.users = User.objects.count()
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'count_user',
                'message':json.dumps(self.users),
            }
        )

   
    
    async def count_user(self, event):
        all_user = User.objects.count()
        await self.send(text_data=json.dumps({
            'message':all_user,
        }))

