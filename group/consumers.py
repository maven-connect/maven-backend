import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import async_to_sync
from channels.db import database_sync_to_async
from .models import Message, Group, PermissionIssueMessage
from django.contrib.auth import get_user_model
from cryptography.fernet import Fernet
import base64
from django.conf import settings
import hashlib

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
    
    def get_group_hash(self, groupName):
        sha256_hash = hashlib.sha256()
        # Encode the input string to bytes and update the hash object
        sha256_hash.update(groupName.encode('utf-8'))
        # Get the hexadecimal representation of the hash
        encrypted_string = sha256_hash.hexdigest()

        return encrypted_string

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
            'type': 'MSG',
        	'timestamp': str(chatMessageObj.timestamp)
        }

    def saveIssuePermissionMessage(self, message, userId, groupName, category):
        userObj = get_user_model().objects.get(email=userId)
        chatObj = Group.objects.get(name=groupName)
        IssuePermissionMsgObj = PermissionIssueMessage.objects.create(
        	group=chatObj, user=userObj, content=message, category=category
        )

        return {
        	'action': 'message',
        	'user': userId,
        	'groupName': groupName,
        	'content': message,
            'type': 'ISP',
            'category': category,
        	'timestamp': str(IssuePermissionMsgObj.timestamp)
        }
            
    async def connect(self):
        try:
            self.userId =  self.scope['user'].id
            self.userSocket = f"chat_{self.userId}"

            self.userGroups = await database_sync_to_async(
		    	list
		    )(Group.objects.filter(users=self.userId))

            for room in self.userGroups:
                await self.channel_layer.group_add(
                	self.get_group_hash(room.name),
                	self.channel_name
                )

            await self.accept()
        except Exception as e:
            print(e)


    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.userSocket, self.channel_name)

    async def receive(self, text_data):
        try:
            text_data_json = json.loads(text_data)
            typeOfMessage = text_data_json["type"]
            message = text_data_json["message"]
            groupName = text_data_json["groupName"]
            sender = text_data_json["sender"]

            if typeOfMessage == "MSG":  

                chatMessage = await database_sync_to_async(
		        		self.saveMessage
		        	)(message, sender, groupName)

                await self.channel_layer.group_send(
                    self.get_group_hash(groupName), {"type": "chat.message", "message":  chatMessage}
                )
            else:
                category = text_data_json["category"]
                IssuePermissionMsg = await database_sync_to_async(
		        		self.saveIssuePermissionMessage
		        	)(message, sender, groupName, category)

                await self.channel_layer.group_send(
                    self.get_group_hash(groupName), {"type": "chat.message", "message":  IssuePermissionMsg}
                )
        except Exception as e:
            print(e)

    async def chat_message(self, event):
        message = event["message"]

        await self.send(text_data=json.dumps({"message": message}))