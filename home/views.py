from django.shortcuts import render
from .models import Pizza,Order
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

def home(request):
    pizza = Pizza.objects.all()
    orders = Order.objects.all()
    print(orders)
    context = {'pizza':pizza,'orders':orders}
    return render(request,'home.html',context)

def order(request,order_id):
    order = Order.objects.get(order_id=order_id)
    context = {'order':order}
    return render(request,'order.html',context)

@csrf_exempt
def order_view(request):
    data = json.loads(request.body)
    pizza = Pizza.objects.get(id=data.get('id'))
    order = Order(pizza=pizza,user=request.user,amount=pizza.price)
    order.save()
    return JsonResponse({'msg':'order received','status':True})
