from django.urls import path, include

from courier_management.views.admin import *

urlpatterns = [
      path('courier_service/',
            CourierServiceViewSet.as_view({'post': 'create', 'get': 'list'},  name='courier_service')),
      path('courier_service/<slug>/',
            CourierServiceViewSet.as_view({'patch': 'update', 'get': 'retrieve'},  name='courier_service')),
      path('delivery_man/',
            DeliveryManViewSet.as_view({'post': 'create', 'get': 'list'},  name='delivery_man')),
      path('delivery_man/<slug>/',
            DeliveryManViewSet.as_view({'patch': 'update', 'get': 'retrieve'},  name='delivery_man')),
]