from django.contrib import admin
from base.models import *
# Register your models here.


class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ['id', 'plan','name', 'created_at']

    class Meta:
        model = Subscription
admin.site.register(Subscription, SubscriptionAdmin)


class PaymentTypeAdmin(admin.ModelAdmin):
    list_display = ['id','name', 'is_active','created_at']

    class Meta:
        model = PaymentType
admin.site.register(PaymentType, PaymentTypeAdmin)



class CompanyTypeAdmin(admin.ModelAdmin):
    list_display = ['id','name', 'is_active','created_at']

    class Meta:
        model = CompanyType
admin.site.register(CompanyType, CompanyTypeAdmin)


class CompanyAdmin(admin.ModelAdmin):
    list_display = ['id','name', 'status','created_at']

    class Meta:
        model = Company
admin.site.register(Company, CompanyAdmin)


class CompanySubscriptionLogAdmin(admin.ModelAdmin):
    list_display = ['id','company', 'created_at']

    class Meta:
        model = CompanySubscriptionLog
admin.site.register(CompanySubscriptionLog, CompanySubscriptionLogAdmin)


class CompanyPaymentLogAdmin(admin.ModelAdmin):
    list_display = ['id','company','created_at']

    class Meta:
        model = CompanyPaymentLog
admin.site.register(CompanyPaymentLog, CompanyPaymentLogAdmin)


class CompanyHistoryAdmin(admin.ModelAdmin):
    list_display = ['id','company','created_at']

    class Meta:
        model = CompanyHistory
admin.site.register(CompanyHistory, CompanyHistoryAdmin)


class TaxCategoryAdmin(admin.ModelAdmin):
    list_display = ['id','name',"slug",'company','created_at']

    class Meta:
        model = TaxCategory
admin.site.register(TaxCategory, TaxCategoryAdmin)

class SMSMailSendLogAdmin(admin.ModelAdmin):
    list_display = ['id','username',"type",'sim_type', 'ip_address','created_at']

    class Meta:
        model = SMSMailSendLog
admin.site.register(SMSMailSendLog, SMSMailSendLogAdmin)
class UserNotificationAdmin(admin.ModelAdmin):
    list_display = ['id','title','created_at']

    class Meta:
        model = UserNotification
admin.site.register(UserNotification, UserNotificationAdmin)