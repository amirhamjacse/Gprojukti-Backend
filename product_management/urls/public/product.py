from django.urls import path
from product_management.views.public.product import *

urlpatterns = [
     path('product/',
          PublicProductViewSet.as_view({'get': 'list'},  name='product')), 
     path('product/<slug>/',
          PublicProductViewSet.as_view({'get': 'retrieve'},  name='product')),
     path('product_attribute_list/<slug>/',
          PublicProductViewSet.as_view({'get': 'product_attribute_list'},  name='product_attribute_list')),
     path('on_the_product_list/<district>/',
          PublicProductViewSet.as_view({'get': 'on_the_product_list'},  name='on_the_product_list')),
     path('on_the_product_wise_shop_list/<district>/<product>/',
          PublicProductViewSet.as_view({'get': 'on_the_product_wise_shop_list'},  name='on_the_product_wise_shop_list')),
     path('active_deals_of_week_product_list/',
          PublicProductViewSet.as_view({'get': 'active_deals_of_week_product_list'},  name='active_deals_of_week_product_list')),
     path('active_campaign_product_list/',
          PublicProductViewSet.as_view({'get': 'active_campaign_product_list'},  name='active_campaign_product_list')),
     path('product_review/<product_slug>/',
          PublicProductViewSet.as_view({'post': 'product_review', 'get': 'product_review_list'},  name='product_review')),   
     path('stock_correction/<product_slug>/',
          PublicProductViewSet.as_view({'post': 'product_review', 'get': 'product_review_list'},  name='product_review')),   

     
]