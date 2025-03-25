from django.urls import path, include

from discount.views.admin import *


urlpatterns = [
    
     path('discount/',
          DiscountViewSet.as_view({'post': 'create', 'get': 'list'},  name='discount')),
     path('discount/<slug>/',
          DiscountViewSet.as_view({'patch': 'update', 'get': 'retrieve', 'delete':'destroy'},  name='discount')),
     path('discount_add_in_product_or_category/<slug>/',
          DiscountViewSet.as_view({'patch': 'discount_add_in_product_or_category'},  name='discount_add_in_product_or_category')),
     path('discount_overview_list/',
          DiscountViewSet.as_view({'get': 'discount_overview_list'},  name='discount_overview_list')),
    
     path('promo_code/',
          PromoCodeViewSet.as_view({'post': 'create', 'get': 'list'},  name='promo_code')),
     path('promo_code/<slug>/',
          PromoCodeViewSet.as_view({'patch': 'update', 'get': 'retrieve', 'delete':'destroy'},  name='promo_code')),
     path('promo_code_add_in_product_or_category/<slug>/',
          PromoCodeViewSet.as_view({'patch': 'promo_code_add_in_product_or_category'},  name='promo_code_add_in_product_or_category')),
     path('promo_code_overview_list/',
          PromoCodeViewSet.as_view({'get': 'promo_code_overview_list'},  name='promo_code_overview_list')),
     
     # Apply Promo Code
     
     path('check_promo_code/',
          PromoCodeViewSet.as_view({'post': 'check_promo_code'},  name='check_promo_code')),
     
    ]
  