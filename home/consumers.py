from channels.generic.websocket import WebsocketConsumer
import json
from asgiref.sync import async_to_sync
from .models import Order

class PizzaConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['order_id']
        self.room_group_name = 'order_%s' %self.room_name 
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()
        data = Order.get_order_details(self.room_name)
        self.send(text_data=json.dumps({
            'payload':data
        }))

    def disconnect(self,close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )