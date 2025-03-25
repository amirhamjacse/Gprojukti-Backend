from django.urls import path, include
from utils.upload_image import image_upload

from product_management.views.admin.category import *

urlpatterns = [
     path('image_upload', image_upload),
     
     path('category_group/',
          CategoryGroupViewSet.as_view({'post': 'create', 'get': 'list'},  name='category_group')),
     path('category_group/<slug>/',
          CategoryGroupViewSet.as_view({'patch': 'update', 'get': 'retrieve', 'delete':'destroy'},  name='category_group')),
     
     path('category/',
          CategoryViewSet.as_view({'post': 'create', 'get': 'list'},  name='category')),
     path('category/<slug>/',
          CategoryViewSet.as_view({'patch': 'update', 'get': 'retrieve', 'delete':'destroy'},  name='category')),
     path('category_overview_list/',
          CategoryViewSet.as_view({'get': 'category_overview_list'},  name='category_overview_list')),
     
     
     # path('category_wise_product_list/',
     #      CategoryViewSet.as_view({'get': 'category_wise_product_list'},  name='category_wise_product_list')),
     
     ]
  