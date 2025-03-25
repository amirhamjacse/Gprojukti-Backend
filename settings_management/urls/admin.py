from django.urls import path
from settings_management.views.admin import *

urlpatterns = [
     path('slider/',
          SliderViewSet.as_view({'get': 'list', "post":"create"},  name='slider')),
     path('slider/<slug>/',
          SliderViewSet.as_view({'patch': 'update', 'get': 'retrieve', 'delete':'destroy'},  name='slider')),
     
     path('shop_day_end/',
          ShopDayEndViewSet.as_view({'get': 'list', "post":"create"},  name='shop_day_end')),
     path('not_shop_day_end_create/',
          ShopDayEndViewSet.as_view({'get': 'not_shop_day_end_create'},  name='not_shop_day_end_create')),
     path('today_shop_sell_details/',
          ShopDayEndViewSet.as_view({'get': 'today_shop_sell_details'},  name='today_shop_sell_details')),
     path('shop_day_end/<slug>/',
          ShopDayEndViewSet.as_view({'patch': 'update', 'get': 'retrieve', 'delete':'destroy'},  name='shop_day_end')),
     path('day_end_message_and_mail/',
          ShopDayEndViewSet.as_view({'get': 'day_end_message_and_mail'},  name='day_end_message_and_mail')),
     
     path('shop_day_end_message/',
          ShopDayEndMessageViewSet.as_view({'get': 'list', "post":"create"},  name='shop_day_end_message')),
     path('shop_day_end_message/<id>/',
          ShopDayEndMessageViewSet.as_view({'patch': 'update', 'get': 'retrieve', 'delete':'destroy'},  name='shop_day_end_message')),
     
     path('shop_panel/',
          ShopPanelViewSet.as_view({'get': 'list', "post":"create"},  name='shop_panel')),
     path('shop_panel/<slug>/',
          ShopPanelViewSet.as_view({'patch': 'update', 'get': 'retrieve'},  name='shop_panel')),
     
     path('shop_panel_hook/',
          ShopPanelHookViewSet.as_view({'get': 'list', "post":"create"},  name='shop_panel_panel')),
     path('shop_panel_hook/<slug>/',
          ShopPanelHookViewSet.as_view({'patch': 'update', 'get': 'retrieve'},  name='shop_panel_hook')),
     
     path('hook_product/',
          HookProductViewSet.as_view({'get': 'list', "post":"create"},  name='shop_panel_panel')),
     path('hook_product/<slug>/',
          HookProductViewSet.as_view({'patch': 'update', 'get': 'retrieve'},  name='shop_panel_hook')),
     
]