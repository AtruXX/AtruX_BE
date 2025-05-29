import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync

class NotificationsConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = 'dispatcher_notifications_channel'

        async_to_sync(self.channel_layer.group_add)(
            self.room_name,
            self.channel_name
        )

        self.accept()
        
        self.send(text_data=json.dumps({
            'type': 'connection_established',
            'message': 'You are now connected to the notifications channel.'
        }))

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_name,
            self.channel_name
        )

    def notify(self, event):
        self.send(text_data=json.dumps({
            'type': 'notification',
            'message': event['data']
        }))
