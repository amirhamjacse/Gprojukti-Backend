from django.urls import path
from product_management.views.public.brand_seller import *

urlpatterns = [
     path('brand/',
          PublicBrandViewSet.as_view({'get': 'list'},  name='brand')), 
]