from django.urls import path, include

from product_management.views.admin.brand_seller import *

urlpatterns = [
     path('brand/',
          BrandViewSet.as_view({'post': 'create', 'get': 'list'},  name='brand')),
     path('brand/<slug>/',
          BrandViewSet.as_view({'patch': 'update', 'get': 'retrieve', 'delete':'destroy'},  name='brand')),
     
     path('supplier/',
          SupplierViewSet.as_view({'post': 'create', 'get': 'list'},  name='supplier')),
     path('supplier/<slug>/',
          SupplierViewSet.as_view({'patch': 'update', 'get': 'retrieve', 'delete':'destroy'},  name='supplier')),
     
     path('seller/',
          SellerViewSet.as_view({'post': 'create', 'get': 'list'},  name='seller')),
     path('seller/<slug>/',
          SellerViewSet.as_view({'patch': 'update', 'get': 'retrieve', 'delete':'destroy'},  name='seller')),
 
    ]
  