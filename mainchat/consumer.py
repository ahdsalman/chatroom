import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from chatapp.models import User
from mainchat.models import Chating
from channels.db import database_sync_to_async

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = self.room_name
        
        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )
        self.accept()

    def disconnect(self, code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )
    
    def create_message(self,content,username,room_name):
        try:
            us_id = int(room_name)
            user = User.objects.get(id=us_id)
            msg = Chating.objects.create(
                room = user,
                content = content,
                username = username
            )
            
            return msg
        except User.DoesNotExist:
            return None

    def receive(self, text_data):
        json_text = json.loads(text_data)
        message = json_text["content"]
        username = json_text["username"]
        
        self.create_message(message, username, self.room_name)
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, 
            {
                "type": "chat_message", 
                "message": message,
                "username":username
            }
        )
    
    def chat_message(self, event):
        message = event['message']
        username = event['username']
        # Send message to WebSocket
        self.send(text_data=json.dumps({"message": message,
                     "username":username}))