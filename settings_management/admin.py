from django.contrib import admin
from settings_management.models import *

# Register your models here.



class SliderAdmin(admin.ModelAdmin):
    list_display = ['id','name', 'is_popup', 'is_slider', 'is_active','created_at']

    class Meta:
        model = Slider
admin.site.register(Slider, SliderAdmin)

class ShopDayEndAdmin(admin.ModelAdmin):
    list_display = ['id','shop', 'total_sell_amount','created_at']
    list_filter = ['shop__name']


    class Meta:
        model = ShopDayEnd
admin.site.register(ShopDayEnd, ShopDayEndAdmin)

class ShopDayEndMessageAdmin(admin.ModelAdmin):
    list_display = ['id','employee_information','created_at']

    class Meta:
        model = ShopDayEndMessage
admin.site.register(ShopDayEndMessage, ShopDayEndMessageAdmin)

class ShopPanelAdmin(admin.ModelAdmin):
    list_display = ['id','name','created_at']

    class Meta:
        model = ShopPanel
admin.site.register(ShopPanel, ShopPanelAdmin)

class ShopPanelHookAdmin(admin.ModelAdmin):
    list_display = ['id','name','created_at']

    class Meta:
        model = ShopPanelHook
admin.site.register(ShopPanelHook, ShopPanelHookAdmin)

class HookProductAdmin(admin.ModelAdmin):
    list_display = ['id','product','created_at']

    class Meta:
        model = HookProduct
admin.site.register(HookProduct, HookProductAdmin)