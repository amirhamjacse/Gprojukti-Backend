from django.contrib import admin
from discount.models import *

# Register your models here.

class DiscountAdmin(admin.ModelAdmin):
    list_display = ['id','name','slug', 'schedule_type', 'amount_type', 'discount_amount','discount_type','discount_status','created_at']

    class Meta:
        model = Discount
admin.site.register(Discount, DiscountAdmin)


class PromoCodeAdmin(admin.ModelAdmin):
    list_display = ['id','promo_code', 'schedule_type', 'amount_type','promo_type','created_at']

    class Meta:
        model = PromoCode
admin.site.register(PromoCode, PromoCodeAdmin)


class PromoCodeLogAdmin(admin.ModelAdmin):
    list_display = ['id','customer', 'promo_code', 'total_apply','created_at']

    class Meta:
        model = PromoCodeLog
admin.site.register(PromoCodeLog, PromoCodeLogAdmin)