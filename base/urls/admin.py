from django.urls import path
from base.views.admin import *

urlpatterns = [
     path('data_set_create/',
          DataViewSet.as_view({'get': 'list'},  name='data_set_create')),
     
     path('subscription/',
          SubscriptionViewSet.as_view({'post': 'create', 'get': 'list'},  name='subscription')),
     path('subscription/<id>/',
          SubscriptionViewSet.as_view({'patch': 'update', 'get': 'retrieve', 'delete':'destroy'},  name='subscription')),
     
     path('company_type/',
          CompanyTypeViewSet.as_view({'post': 'create', 'get': 'list'},  name='company_type')),
     path('company_type/<id>/',
          CompanyTypeViewSet.as_view({'patch': 'update', 'get': 'retrieve', 'delete':'destroy'},  name='company_type')),
     
     path('payment_type/',
          PaymentTypeViewSet.as_view({'post': 'create', 'get': 'list'},  name='payment_type')),
     path('payment_type/<id>/',
          PaymentTypeViewSet.as_view({'patch': 'update', 'get': 'retrieve', 'delete':'destroy'},  name='payment_type')),
     
     path('company/',
          CompanyViewSet.as_view({'post': 'create', 'get': 'list'},  name='company')),
     path('company/<id>/',
          CompanyViewSet.as_view({'patch': 'update', 'get': 'retrieve', 'delete':'destroy'},  name='company')),
     path('user_company_profile/',
          CompanyViewSet.as_view({'get': 'user_company_profile'},  name='user_company_profile')),
     
     path('tax_category/',
          TaxCategoryViewSet.as_view({'post': 'create', 'get': 'list'},  name='tax_category')),
     path('tax_category/<slug>/',
          TaxCategoryViewSet.as_view({'patch': 'update', 'get': 'retrieve', 'delete':'destroy'},  name='tax_category')),
     
     path('sms_mail_log/',
          SMSMailSendLogViewSet.as_view({'get': 'list'},  name='sms_mail_log')),
     path('sms_mail_log/<id>/',
          SMSMailSendLogViewSet.as_view({'get': 'retrieve'},  name='sms_mail_log')),
     
     
     path('user_notification/',
          UserNotificationViewSet.as_view({'get': 'list'},  name='user_notification')),
     path('user_notification/<id>/',
          UserNotificationViewSet.as_view({'get': 'retrieve'},  name='user_notification')),
     
     # path('user_activity/',
     #      UserActivityLogViewSet.as_view({'get': 'list'},  name='user_activity')),
     # path('user_activity/<id>/',
     #      UserActivityLogViewSet.as_view({'get': 'retrieve'},  name='user_activity')),
]