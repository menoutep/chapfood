import json
from channels.generic.websocket import AsyncWebsocketConsumer
from api.serializers import OrderSerializer
from asgiref.sync import async_to_sync

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        await self.channel_layer.group_add("notifications", self.channel_name)

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("notifications", self.channel_name)

    async def send_notification(self, event):
        message = event["message"]

        await self.send(text_data=json.dumps({
            "type": "notification",
            "message": message
        }))
# consumers.py



class NotificationType1Consumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        await self.channel_layer.group_add("notifications_type1", self.channel_name)

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("notifications_type1", self.channel_name)

    async def send_notification_type1(self, event):
        message = event["message"]
        # Log pour vérifier si les données sont reçues correctement
        print(f"Sending notification: {message}")
        # Envoie les données actualisées aux clients WebSocket connectés
        await self.send(text_data=json.dumps({
            "type": "notification_type1",
            "message": message
        }))


# consumers.py


class NotificationType2Consumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        await self.channel_layer.group_add("notifications_type2", self.channel_name)

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("notifications_type2", self.channel_name)

    async def send_notification_type2(self, event):
        message = event["message"]
        print(f"Sending notification: {message}")
        # Envoie la notification de type 2 au client
        await self.send(text_data=json.dumps({
            "type": "notification_type2",
            "message": message
        }))



class NotificationType3Consumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        await self.channel_layer.group_add("notifications_type3", self.channel_name)

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("notifications_type3", self.channel_name)

    async def send_notification_type3(self, event):
        message = event["message"]
        print(f"Sending notification: {message}")
        # Envoie la notification de type 3 au client
        await self.send(text_data=json.dumps({
            "type": "notification_type3",
            "message": message
        }))
