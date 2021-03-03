from django.db import models
import string
import random
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json

class Pizza(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField(default=0)
    image = models.ImageField(upload_to='pizza/')

    def __str__(self):
        return self.name

def random_string_generator(size=10,chars=string.ascii_lowercase+string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

CHOICES = (
    ('order received','order received'),
    ('Baking','Baking'),
    ('Baked','Baked'),
    ('Out for delivery','Out for delivery'),
    ('order Received','order Received'),
)

class Order(models.Model):
    pizza = models.ForeignKey(Pizza,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    order_id = models.CharField(max_length=100,blank=True)
    amount = models.FloatField()
    status = models.CharField(max_length=20,choices=CHOICES,default='order received')
    created_at = models.DateTimeField(auto_now_add=True)


    def save(self,*args,**kwargs):
        if not self.order_id:
            self.order_id = random_string_generator()
        super(Order,self).save(*args,**kwargs)

    @staticmethod
    def get_order_details(order_id):
        instance = Order.objects.filter(order_id=order_id).first()
        data = {}
        progress = 0
        data['status'] = instance.status
        if instance.status == "order received":
            progress = 20
        elif instance.status == "Baking":
            progress = 40
        elif instance.status == "Baked":
            progress = 60
        elif instance.status == "Out for delivery":
            progress = 80
        elif instance.status == "order Received":
            progress = 100
        data['progress'] = progress
        return data

@receiver(post_save,sender=Order)
def order_status_update(sender,instance,created,**kwargs):
    if not created:
        channel_layer = get_channel_layer()
        data = {}
        progress = 0
        data['status'] = instance.status
        if instance.status == "order received":
            progress = 20
        elif instance.status == "Baking":
            progress = 40
        elif instance.status == "Baked":
            progress = 60
        elif instance.status == "Out for delivery":
            progress = 80
        elif instance.status == "order Received":
            progress = 100
        data['progress'] = progress

        async_to_sync(channel_layer.group_send)(
            'order_%s' %instance.order_id,{
                'type':'order_status',
                'value':json.dumps(data)
            }
        )

        