from django.urls import path
from user.views.admin import AdminUserViewSet
from user.views.public import LoginViewSet, UserViewSet

urlpatterns = [
     path('login/', LoginViewSet.as_view({'post':'create'}), name='login'),
     path('get_otp/<str:username>/',
          UserViewSet.as_view({'get': 'get_otp'},  name='get_otp')),
     path('update_password/', 
          UserViewSet.as_view({'patch':'update_password'}), name='update_password'),
     path('profile/', 
          UserViewSet.as_view({'get':'user_profile'}), name='user_profile'),
     path('user/',
          UserViewSet.as_view({'post': 'create'},  name='user')),
     path('google_signup/',
          UserViewSet.as_view({'post': 'google_signup'},  name='google_signup')),
     path('captcha_login/',
          UserViewSet.as_view({'post': 'captcha_login'},  name='captcha_login')),
     path('user_profile_update/',
          UserViewSet.as_view({'patch': 'update'},  name='user_profile_update')),
]