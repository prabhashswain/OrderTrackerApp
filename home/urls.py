from django.urls import path
from .views import home,order_view,order

urlpatterns = [
    path('',home,name='home'),
    path('order/<order_id>/',order,name='order'),
    path('api/order',order_view,name='api-order'),
]