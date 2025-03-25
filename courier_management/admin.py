from django.contrib import admin
from courier_management.models import *

# Register your models here.

class CourierServiceAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']

    class Meta:
        model = CourierService
admin.site.register(CourierService, CourierServiceAdmin)


class DeliveryManAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']

    class Meta:
        model = DeliveryMan
admin.site.register(DeliveryMan, DeliveryManAdmin)


class CourierAdmin(admin.ModelAdmin):
    list_display = ['id', 'order']

    class Meta:
        model = Courier
admin.site.register(Courier, CourierAdmin)


class CourierStatusLogAdmin(admin.ModelAdmin):
    list_display = ['id', 'courier']

    class Meta:
        model = CourierStatusLog
admin.site.register(CourierStatusLog, CourierStatusLogAdmin)