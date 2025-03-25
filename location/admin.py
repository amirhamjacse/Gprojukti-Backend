from django.contrib import admin
from location.models import *

# Register your models here.

class CountryAdmin(admin.ModelAdmin):
    list_display = ['id','name','created_at']

    class Meta:
        model = Country
admin.site.register(Country, CountryAdmin)

class DivisionAdmin(admin.ModelAdmin):
    list_display = ['id','name','slug', 'country','created_at']

    class Meta:
        model = Division
admin.site.register(Division, DivisionAdmin)

class DistrictAdmin(admin.ModelAdmin):
    list_display = ['id','name', 'slug','division','created_at']

    class Meta:
        model = District
admin.site.register(District, DistrictAdmin)

class AreaAdmin(admin.ModelAdmin):
    list_display = ['id','name','slug','district','created_at']

    class Meta:
        model = Area
admin.site.register(Area, AreaAdmin)

class POSAreaAdmin(admin.ModelAdmin):
    list_display = ['id','name', 'district','created_at']

    class Meta:
        model = POSArea
admin.site.register(POSArea, POSAreaAdmin)

class POSRegionAdmin(admin.ModelAdmin):
    list_display = ['id','name','created_at']

    class Meta:
        model = POSRegion
admin.site.register(POSRegion, POSRegionAdmin)

class OfficeLocationAdmin(admin.ModelAdmin):
    list_display = ['id','name', 'primary_phone', 'slug','is_use_scanner', 'area','office_type','created_at']

    class Meta:
        model = OfficeLocation
        
admin.site.register(OfficeLocation, OfficeLocationAdmin)
