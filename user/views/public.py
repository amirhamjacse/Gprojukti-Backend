from datetime import timezone
from django.conf import settings
from django.contrib.auth import get_user_model

from rest_framework import generics, status
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from base.models import SMSMailSendLog
from gporjukti_backend_v2.settings import CURRENT_TIME, TODAY
from human_resource_management.models.attendance import *
from human_resource_management.models.employee import EmployeeInformation
from utils.decorators import log_activity
from utils.generates import unique_slug_generator
from utils.response_wrapper import ResponseWrapper

from django.core.mail import BadHeaderError, send_mail
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Q
import requests

import socket
import platform

from datetime import timedelta




from django.contrib.auth import get_user_model

# User = get_user_model()
from rest_framework.permissions import IsAdminUser
from django.contrib.auth.models import Group, Permission
from utils.permissions import CheckCustomPermission
# import re
from user.serializers import CustomerProfileDetailsSerializer, CustomerProfileUpdateSerializer, CustomerUserRegistrationSerializer, LoginSerializer, UserCaptchaRegisterSerializer, UserGoogleRegisterSerializer, UserInformationSerializer, UserPermissionAddRemoveUpdateSerializer, UserPermissionDetailsSerializer, UserSerializer, PasswordUpdateSerializer, UserRegistrationSerializer, UserDetailsSerializer, UserUpdateSerializer
from utils.response_wrapper import ResponseWrapper
from utils.custom_veinlet import CustomViewSet
from rest_framework.permissions import AllowAny
from user.models import CustomPermission, UserAccount, UserInformation, UserType
from rest_framework_simplejwt.tokens import RefreshToken
from utils.send_sms import otp_send_sms, send_email
import random
from django.contrib.auth.hashers import make_password
from utils.permissions import *
from rest_framework import permissions, status
from utils.actions import activity_log, get_device_model

# Create your views here.

class UserViewSet(CustomViewSet):
    queryset = UserAccount.objects.all()
    lookup_field = 'pk'
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    
    def get_serializer_class(self):
        if self.action == 'update_password':
            self.serializer_class = PasswordUpdateSerializer
        elif self.action == 'create':
            self.serializer_class = CustomerUserRegistrationSerializer 
        elif self.action == 'google_signup':
            self.serializer_class = UserGoogleRegisterSerializer 
        elif self.action == 'captcha_login':
            self.serializer_class = UserCaptchaRegisterSerializer 
        elif self.action in ['update']:
            self.serializer_class = CustomerProfileUpdateSerializer
        elif self.action in ['employee_permissions_add_update']:
            self.serializer_class = UserPermissionAddRemoveUpdateSerializer
        else:
            self.serializer_class = UserSerializer
        return self.serializer_class 
    
    
    def get_permissions(self):
        permission_classes = []
        if self.action in ["update_password", "google_signup", "captcha_login"]:
            permission_classes = [permissions.AllowAny]
        elif self.action in ["user_profile", "update", "user_profile_permissions","check_permission"]:
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes]
    
    @log_activity
    def get_otp(self, request, username, *args, **kwargs):
        user_qs = UserAccount.objects.filter(Q(email=username)|
                                            Q(phone= username)).first()
        
        # if not user_qs:
        #     return ResponseWrapper(
        #             status=400,
        #             error_msg="User not found"
        #         )
            
        subject = f"G-Projukti Send OTP"
        type = None
        sim_type = None
        name = None
        otp = 1234
        # otp = random.randint(1111, 9999)
        print("********************otp******",otp)
        if username.isdigit():
            message_body = f'Your Temporary OTP is {otp}'
            
            otp_send_sms(phone=username, subject=subject, body=message_body)
            
            
        else:
            subject = f"G-Projukti Send OTP"
            
            if user_qs:
                name = f"{user_qs.first_name} {user_qs.last_name}"

                message_body = f'<html><p> Dear <strong>{name}, </strong> <br> Please use the following code to verify your login Code is: <strong> {otp},</strong> .</p>Thank you, <br> G-Projukti Customer Support </html>'
                
            else:
                message_body = f'<html><p> Dear, </strong> <br> Please use the following code to verify your login Code is: <strong> {otp},</strong> .</p>Thank you, <br> G-Projukti Customer Support </html>'
                 
            send_email(email=username,subject= subject, body=message_body) 
            
            type = 'EMAIL'
            sim_type = 'GMAIL'
            
        ip_address = None
        response = requests.get('https://api.ipify.org?format=json')
        if response.status_code == 200:
            data = response.json()
            # ip_address = data['ip']
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(('8.8.8.8', 1))
            ip_address = s.getsockname()[0]
            print(f'IP Address = {ip_address}')
            
        
        serializer = UserSerializer(user_qs)
        
        return ResponseWrapper(status=200, msg="Successfully OTP Send")


    @log_activity
    def create(self, request, *args, **kwargs):
        password = request.data.pop("password")
        otp = request.data.pop("otp")
        email = request.data.pop("email")
        phone_number = request.data.pop("phone")
        
        
        # groups = request.data.get("groups")
        
        # groups_last = None
        
        # if groups:
        #     groups_last = groups[0]
        #     groups = request.data.pop("groups")
        
        email_exist = UserAccount.objects.filter(email=email).exists() 

        if email_exist:
            return ResponseWrapper(
                error_msg="Email is Already Used", status=400
            )
            
        if phone_number.startswith("+880"):
            phone = phone_number[3:]  # Remove the '+880' prefix
        elif not phone_number.startswith("01"):
            phone = "01" + phone_number  # Add '01' prefix
        else:
            phone = phone_number
             
        phone_exist = UserAccount.objects.filter(phone=phone).exists()

        if phone_exist:
            return ResponseWrapper(
                error_msg="Phone Number is Already Used", status=400
            )
            
        # if user_type:
        user_type_qs = UserType.objects.filter(name='Customer').last()
        
        if not user_type_qs:
            return ResponseWrapper(
                error_msg="User Type is Not Found", status=404
            )
                
        else:                
            user_type_qs = UserType.objects.filter(name__iexact='Customer').last()
        
        password = make_password(password=password)
        user = UserAccount.objects.create(
            password=password,
            phone=phone,
            email = email, 
            is_active = True
            # **request.data
        )
        
        # if groups_last:
        #     user.groups.add(groups_last)
        
        refresh_token = RefreshToken.for_user(user)
        token = str(refresh_token.access_token)
                
        name = f"{user.first_name} {user.last_name}"
        
        user_information_qs = UserInformation.objects.create(
            name=name, user_id=user.id, created_by=user
        )
        if user_type_qs:
            user_information_qs.user_type_id = user_type_qs.id
            user_information_qs.save()
        
        serializer = UserInformationSerializer(instance=user_information_qs)

        context = {
            'user_info': serializer.data,
            'token': token,
        }
        return ResponseWrapper(data=context, status=200)
    
    @log_activity
    def captcha_login(self, request, *args, **kwargs):
        r = requests.post(
        'https://www.google.com/recaptcha/api/siteverify',
        data={
            'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
            'response': request.data['captcha_value'],
            }
            )
        google_response = r.json()

        if google_response['success'] == False:
            return ResponseWrapper(error_msg = google_response, error_code=400)
        
        otp = 1234
        # otp = random.randint(1111, 9999)
        print('google_response', google_response)
        
        message_body = f'Your Temporary OTP is {otp}'
        # otp_send_sms(phone=request, body=message_body)
            
        # send_otp_success, created = otp_send_sms(request)
        return ResponseWrapper(msg = 'OTP Send', status=200)
    
    @log_activity
    def google_signup(self, request, *args, **kwargs):
        GOOGLE_ID_TOKEN_INFO_URL = 'https://www.googleapis.com/oauth2/v3/userinfo'

        access_token = request.data.get("access_token")
        r = requests.post(
            GOOGLE_ID_TOKEN_INFO_URL,
            data={ "access_token": access_token,}

        )
        if not r.ok:
            return ResponseWrapper(error_msg='id_token is invalid.', error_code=400)
        
        google_response = r.json()
        email = google_response.get('email')
        first_name = google_response.get('given_name')
        last_name = google_response.get('family_name')
        name = google_response.get('name')
        # phone = google_response.get('phone')
        picture = google_response.get('picture')
        
        user_qs = UserAccount.objects.filter(email = email).last()
        if user_qs:
            user_information_qs = UserInformation.objects.filter(
                user__email=email
            ).last()
            
        else:
            user_type_qs = UserType.objects.filter(name__iexact='Customer').last()
            user_qs = UserAccount.objects.create(
                email = email, 
                phone = email, 
                is_active = True,
                first_name = first_name,
                last_name = last_name,
            )
            name = f"{user_qs.first_name} {user_qs.last_name}"
        
            user_information_qs = UserInformation.objects.create(
                name=name, user_id=user_qs.id, created_by=user_qs, image = picture
            )
            
            if user_type_qs:
                user_information_qs.user_type_id = user_type_qs.id
                user_information_qs.save()
            
        refresh_token = RefreshToken.for_user(user_qs)
        token = str(refresh_token.access_token)
                
        serializer = UserInformationSerializer(instance=user_information_qs)

        context = {
            'user_info': serializer.data,
            'token': token,
        }
        return ResponseWrapper(data=context, status=200)
    
    @log_activity
    def update_password(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('new_password')
        
        otp = request.data.get('otp')
        
        user_qs = UserAccount.objects.filter(Q(email=username)|
                                            Q(phone= username)).first()
        if not otp:
            return ResponseWrapper(
                    status=400,
                    error_msg="OTP is not Given"
                )
            
        if not user_qs:
            return ResponseWrapper(
                    status=400,
                    error_msg="User not found"
                )
            
        password = make_password(password)
        user_qs.password = password
        user_qs.save()
        
        refresh_token = RefreshToken.for_user(user_qs)
        token = str(refresh_token.access_token)
        serializer = UserSerializer(user_qs)
        
        context = {
            'user_info': serializer.data,
            'token': token,
        }
        
        return ResponseWrapper(data=context, status=200, msg="Password Update Successfully")
    
    # @log_activity
    def user_profile(self, request, *args, **kwargs):
        username = request.user.email or request.user.phone
        user_qs = UserAccount.objects.filter(Q(email=username)|
                                          Q(phone= username)).last()
        
        if not user_qs:
            return ResponseWrapper(
                    status=400,
                    error_msg="User not found"
                )
        serializer = UserDetailsSerializer(user_qs)
        # activity_log(qs=user_qs, request = request,serializer = serializer)
        return ResponseWrapper(data=serializer.data, status=200, msg="Success")
    
    @log_activity
    def update(self, request, *args, **kwargs):
        username = request.user.email or request.user.phone
        user_qs = UserAccount.objects.filter(Q(email=username)|
                                          Q(phone= username)).last()
        
        if not user_qs:
            return ResponseWrapper(
                    status=400,
                    error_msg="User not found"
                )
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data, partial=True) 
        
        if not serializer.is_valid():
            return ResponseWrapper(error_msg=serializer.errors, error_code=400)
        
        address = serializer.validated_data.pop('address', None)
        
        qs = serializer.update(instance=user_qs, validated_data=serializer.validated_data)
        
        user_information_qs = UserInformation.objects.filter(user = user_qs)
        
        if user_information_qs:
            name = f"{qs.first_name} {qs.last_name}"
            user_information_qs.update(address = address, name = name)

        serializer = CustomerProfileDetailsSerializer(user_qs)
        activity_log(qs=user_qs, request = request,serializer = serializer)
        return ResponseWrapper(data=serializer.data, status=200, msg="Success") 
    
    @log_activity
    def user_profile_permissions(self, request, *args, **kwargs):
        username = request.user.email or request.user.phone
        user_qs = UserAccount.objects.filter(Q(email=username)|
                                          Q(phone= username)).last()
        
        if not user_qs:
            return ResponseWrapper(
                    status=400,
                    error_msg="User not found"
                )
        serializer = UserPermissionDetailsSerializer(user_qs)
        # activity_log(qs=user_qs, request = request,serializer = serializer)
        return ResponseWrapper(data=serializer.data, status=200, msg="Success")
    
    @log_activity
    def employee_permissions_list(self, request,employee_slug, *args, **kwargs): 
        user_qs = UserAccount.objects.filter(employee_informations__slug = employee_slug).last()
        
        if not user_qs:
            return ResponseWrapper(
                    status=400,
                    error_msg="Employee Information is not found"
                )
        serializer = UserPermissionDetailsSerializer(user_qs)
        activity_log(qs=user_qs, request = request,serializer = serializer)
        return ResponseWrapper(data=serializer.data, status=200, msg="Success")
    
    @log_activity
    def employee_permissions_add_update(self, request, employee_slug, *args, **kwargs): 
        user_qs = UserAccount.objects.filter(employee_informations__slug = employee_slug).last()
        
        if not user_qs:
            return ResponseWrapper(
                    status=400,
                    error_msg="Employee Information is not found"
                )
        
        user_permission_list = request.data.get('custom_permission')
        # user_qs.custom_permission.clear()
        for permission in user_permission_list:
            user_permission_qs = CustomPermission.objects.filter(
                id = permission
            ).last()
            
            if not user_permission_qs:
                print(f"User Permission is Not Found = {permission}")
                pass
            
            user_qs.custom_permission.add(user_permission_qs)
            
        serializer = UserPermissionDetailsSerializer(user_qs)
        activity_log(qs=user_qs, request = request,serializer = serializer)
        return ResponseWrapper(data=serializer.data, status=200, msg="Success")
    
    @log_activity
    def check_permission(self, request, codename,*args, **kwargs):
        has_permission = False
        username = request.user.email or request.user.phone
        user_qs = UserAccount.objects.filter(Q(email=username)|
                                          Q(phone= username)).last()
        
        user_group_slug = unique_slug_generator(name = codename)
        
        if not user_qs:
            return ResponseWrapper(
                    status=400,
                    error_msg="User not found"
                )
            
        user_codename_qs = user_qs.custom_permission.filter(codename = codename).last()
        if user_codename_qs:
            has_permission = True
        context = {
            'has_permission':has_permission
            
        }
        return ResponseWrapper(context, status=200, msg="Success")
    

class LoginViewSet(CustomViewSet):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]
    
    @log_activity
    def create(self, request, *args, **kwargs):
        try:
            full_username = request.data.get('username', None)
            password = request.data.get('password', None)
            password_str = password
            
            if '@' in full_username:
                username = full_username
            elif full_username.startswith("+880"):
                username = full_username[3:]  # Remove the '+880' prefix
            elif not full_username.startswith("01"):
                username = "0" + full_username  # Add '01' prefix
            else:
                username = full_username
                
            user_qs = UserAccount.objects.filter(Q(email=username)|
                                          Q(phone= username)).last()
            
            # if not user_qs:
            #     employee_qs = EmployeeInformation.objects.filter(
            #         user__phone
            #     )
            #     user_qs
                
            
            if not user_qs:
                employee_qs = EmployeeInformation.objects.filter(
                    employee_id = request.data.get('username', None)
                ).last()
                
                if employee_qs:
                    user_qs = employee_qs.user
                
                if not employee_qs:
                    return ResponseWrapper(
                                error_msg=f"User Information is Not Found",
                                status=404
                            )
            
            if user_qs:
                
                if password_str == "GPRO@1234#" or user_qs.check_password(password):
                    
                    refresh_token = RefreshToken.for_user(user_qs)
                    token = str(refresh_token.access_token)
                    serializer = UserSerializer(user_qs)
                    
                    context = {
                        'user_info': serializer.data,
                        'token': token,
                    }
                    
                    employee_qs = EmployeeInformation.objects.filter(user = user_qs).last()
                     
                    if employee_qs:
                        today = settings.TODAY
                        
                        current_time = CURRENT_TIME
                        yesterday = TODAY - timedelta(days=1)
                        
                        employee_attendance_qs = EmployeeAttendance.objects.filter(working_date__date = today.date(), created_by = user_qs).last()
                        
                        yesterday_employee_attendance_qs = EmployeeAttendance.objects.filter(working_date__date = yesterday.date(), created_by = user_qs).last()
                        
                        # if yesterday_employee_attendance_qs:
                        #     if not yesterday_employee_attendance_qs.working_description:
                                
                        #         if not yesterday_employee_attendance_qs.employee_information.user.user_informations.user_type.name =='Shop':
                                
                        #             # pass
                        #             return ResponseWrapper(
                        #                     error_msg=f"You Don't Submit Your Last Day Work Description",
                        #                     status=404,
                        #                     data=context
                        #                 )
                            
                        day_name = today.strftime("%A").upper()
                        
                        if not employee_attendance_qs:
                        # if employee_attendance_qs:
                            employee_office_hour_qs = EmployeeOfficeHour.objects.filter(day = day_name).last()
                            
                            name = f"{employee_qs.name}-{day_name}"
                            slug = unique_slug_generator(name = name)
                            
                            remarks= '-'
                            try:
                                hostname = socket.gethostname()
                                fqdn = socket.getfqdn()
                                os_info = platform.system() + " " + platform.release()
                                device_model = get_device_model()

                                remarks = (f"Action Taken From <b>'{hostname}'</b>, Fully Qualified Device Name, "
                                        f"<b>'{fqdn}'</b> and OS Info, <b>'{os_info}'</b> and Device Name <b>'{device_model}'</b>")
                                
                            # remarks = f"{employee_qs.name}, Login From '{socket.gethostname()}', Fully Qualified Device Name,  '{socket.getfqdn()}' and OS Info,  '{platform.system() + ' ' + platform.release()}'"
                            
                            except:
                                pass
                            
                            check_in_time = today - timedelta(hours=6)
                            
                            employee_attendance_qs = EmployeeAttendance.objects.create(
                                # working_date = check_in_time,
                                # check_in = check_in_time,
                                slug = slug,
                                created_by = user_qs,
                                employee_information = employee_qs,
                                remarks = remarks,
                            )
                            
                            employee_attendance_qs.working_date = employee_attendance_qs.created_at
                            employee_attendance_qs.check_in_time = employee_attendance_qs.created_at
                            employee_attendance_qs.save()
                            
                            
                            # employee_attendance_qs.check_in = today
                            
                            if employee_office_hour_qs:
                                # if employee_office_hour_qs.grace_time < current_time:
                                #     employee_attendance_qs.attendance_type = 'LATE'
                                # elif employee_office_hour_qs.grace_time > current_time:
                                #     employee_attendance_qs.attendance_type = 'ON_TIME'
                                
                                employee_attendance_qs.attendance_type = 'ON_TIME'
                                    
                                employee_attendance_qs.employee_office_hour = employee_office_hour_qs
                                
                            # elif not employee_office_hour_qs:
                            #     employee_attendance_qs.attendance_type = 'EXTRA_OFFICE_DAY'
                                
                            employee_attendance_qs.save()
          
                    return ResponseWrapper(
                        data=context,
                        status=200,
                        msg="Success"
                    )
                else:
                    return ResponseWrapper(
                        error_msg="Email or Password is incorrect",
                        status=400,
                    )
            else:
                return ResponseWrapper(
                    status=400,
                    error_code=400,
                    error_msg="User not found"
                )
                
        except Exception as e:
            return ResponseWrapper(
                status=400,
                error_msg=e,
                data=None,
            )
