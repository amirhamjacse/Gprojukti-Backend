from django.urls import path
from product_management.views.public.category import *

urlpatterns = [
     path('category/',
          PublicCategoryViewSet.as_view({'get': 'list'},  name='category')), 
     path('category/<slug>/',
          PublicCategoryViewSet.as_view({'get': 'retrieve'},  name='category')), 
     path('category_group/',
          PublicCategoryGroupViewSet.as_view({'get': 'list'},  name='category_group')), 
     path('category_group/<slug>/',
          PublicCategoryGroupViewSet.as_view({'get': 'retrieve'},  name='category_group')), 
     
]