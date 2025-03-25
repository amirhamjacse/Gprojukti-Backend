from django.contrib import admin
from user.models import *

# Register your models here.

# ................***...............Profile................***............

class UserAccountAdmin(admin.ModelAdmin):
    list_display = ['id','first_name', 'last_name', 'email','phone', 'is_active']

    class Meta:
        model = UserAccount
admin.site.register(UserAccount, UserAccountAdmin)

class UserTypeAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'slug']

    class Meta:
        model = UserType
admin.site.register(UserType, UserTypeAdmin)

class UserInformationAdmin(admin.ModelAdmin):
    list_display = ['id', 'name','user', 'user_type']
    list_filter = ['user_type__name']


    class Meta:
        model = UserInformation
admin.site.register(UserInformation, UserInformationAdmin)

class CustomPermissionAdmin(admin.ModelAdmin):
    list_display = ['id', 'name','model_name', 'codename', 'is_active']

    class Meta:
        model = CustomPermission
admin.site.register(CustomPermission, CustomPermissionAdmin)

class UserGroupAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']

    class Meta:
        model = UserGroup
admin.site.register(UserGroup, UserGroupAdmin)

# class BaseModelAdmin(admin.ModelAdmin):
#     list_display = ['id', 'created_by', 'updated_by', 'created_at', 'updated_at']

#     class Meta:
#         model = BaseModel
# admin.site.register(BaseModel, BaseModelAdmin)