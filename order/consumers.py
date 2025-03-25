from asyncio.log import logger
import json
import logging
import json
from channels.generic.websocket import AsyncWebsocketConsumer

class OrderNotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        # Handle WebSocket messages here
        text_data_json = json.loads(text_data)
        # message = text_data_json["message"]

        # # await self.send(text_data=json.dumps({"Message from the server: ": message}))
        # if message:
        #     await self.send(text_data=json.dumps({"Message from the server: ": message}))
        message_type = text_data_json.get("type")
        if message_type == "join_group":
            group_name = text_data_json.get("group_name")
            print(f"group_name", group_name)
            
            if group_name:
                await self.join_group(group_name)
                
    async def join_group(self, group_name):
        # Add the user to the specified group
        await self.channel_layer.group_add(
            group_name,      # Group name received from the message
            self.channel_name  # Channel name associated with this WebSocket connection
        )
        
    async def send_notification(self, event):
        # This method will handle the WebSocket message
        data = event["data"]
        await self.send(text_data=json.dumps({"order_data": data}))
        
