from django.urls import path, include

from order.views.admin import DeliveryMethodViewSet, OrderViewSet
from order.views.public import PublicOrderViewSet

urlpatterns = [
        path('order/',
            PublicOrderViewSet.as_view({'post': 'create', 'get': 'list'},  name='order')),
        path('order_details/<invoice_no>/',
            PublicOrderViewSet.as_view({'get': 'order_details'},  name='order_details')),
        path('ssl_order_payment/<invoice_no>/',
            PublicOrderViewSet.as_view({'get': 'ssl_order_payment'},  name='ssl_order_payment')),
    
        path('delivery_method/',
                DeliveryMethodViewSet.as_view({'get': 'list'},  name='delivery_method')),
        path('order_payment_details/<invoice_no>/',
            OrderViewSet.as_view({'get': 'order_payment_details'},  name='order_payment_details')),
        ]
  