import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import async_to_sync
from channels.db import database_sync_to_async
from .models import Message, Group
from django.contrib.auth import get_user_model

class ChatConsumer(AsyncWebsocketConsumer):
    @database_sync_to_async
    def get_group(self, groupName):
        group = Group.objects.get(name=groupName)
        return group

    @database_sync_to_async
    def get_group_users(self, group):
        userList = group.users.all()
        return userList
    
    @database_sync_to_async
    def get_user_groups(self, user):
        return user.group_set.all()
    
    def saveMessage(self, message, userId, groupName):
        userObj = get_user_model().objects.get(email=userId)
        chatObj = Group.objects.get(name=groupName)
        chatMessageObj = Message.objects.create(
        	group=chatObj, user=userObj, content=message
        )
        return {
        	'action': 'message',
        	'user': userId,
        	'groupName': groupName,
        	'content': message,
        	'timestamp': str(chatMessageObj.timestamp)
        }
            
    async def connect(self):
        # self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.userId =  self.scope['user'].id
        # self.room_group_name = f"chat_{self.room_name}"
        self.userSocket = f"chat_{self.userId}"
        
        self.userGroups = await database_sync_to_async(
			list
		)(Group.objects.filter(users=self.userId))
        
        for room in self.userGroups:
            await self.channel_layer.group_add(
            	room.name,
            	self.channel_name
            )

        # await self.channel_layer.group_add(self.userSocket, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.userSocket, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        groupName = text_data_json["groupName"]
        sender = text_data_json["sender"]

        chatMessage = await database_sync_to_async(
				self.saveMessage
			)(message, sender, groupName)

        await self.channel_layer.group_send(
            groupName, {"type": "chat.message", "message":  chatMessage}
        )

    async def chat_message(self, event):
        message = event["message"]

        await self.send(text_data=json.dumps({"message": message}))