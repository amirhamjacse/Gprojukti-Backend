from human_resource_management.models.employee import *
from location.models import *
from user.models import *
from django.db.models import Q
from django.contrib.auth.hashers import make_password

image_1 = 'https://static.vecteezy.com/system/resources/thumbnails/029/938/693/small_2x/3d-cartoon-cute-boy-photo.jpg'

image_2 = 'https://i.pinimg.com/236x/8e/6b/42/8e6b420566037a1177f5adb767cb2318.jpg'


def multiple_employee_create(employee_list, request_user):
    count = 20
    
    for item in employee_list:
        email = item.get('email')
        phone = item.get('phone')
        password = item.get('password')
        first_name = item.get('first_name')
        last_name = item.get('last_name')
        is_superuser = item.get('is_superuser')
        user_type = item.get('user_type')
        
        if count % 2 == 0:
            image = image_1
        else:
            image = image_2
        
        qs = UserAccount.objects.filter(Q(email = email) | Q(phone = phone)).last()
        
        if qs:
            qs.first_name = first_name
            qs.last_name = last_name
            # qs.email = email
            # qs.phone = phone
            qs.is_superuser = is_superuser
            # qs.save()
        else:
            password = make_password(password=password)
            
            qs = UserAccount.objects.create(
                first_name=first_name,
                last_name = last_name,
                email = email,
                phone = phone,
                is_superuser = is_superuser,
                password = password
                # created_by = request_user
                )
            
        name = f"{qs.first_name} {qs.last_name}"
        
        user_information_qs = UserInformation.objects.filter(user_id=qs.id).last()
        user_type_qs = UserType.objects.filter(name = user_type).last()
        
        if not user_information_qs:
            user_information_qs = UserInformation.objects.create(
            name=name,image=image,  user_id=qs.id, created_by=request_user
        )
        else:
            user_information_qs.image = image
            user_information_qs.save()
            
        if user_type_qs:
            user_information_qs.user_type_id = user_type_qs.id
            user_information_qs.save()
            
        employee_information_qs = EmployeeInformation.objects.filter(user_id=qs.id)
        
        employee_id =  f'GPRO-000{count}'
        nid_number =  f'8765445000{count}'
        passport_number =  f'98765456{count}'
        
        
        company_qs = Company.objects.filter(name__icontains = 'Gprojukti .com').last()
        employee_type_qs = EmployeeType.objects.filter(name__icontains = 'Full Time').last()
        designation_qs = Designation.objects.all().order_by('?').last()
            
        
        if not employee_information_qs:
            
            slug = unique_slug_generator(name = name)
            employee_information_qs = EmployeeInformation.objects.create(
                employee_id = employee_id, name=name,
                image=image, slug = slug, phone_number = phone, 
                user_id=qs.id, employee_company_id = company_qs.id, designations_id = designation_qs.id, employee_type_id = employee_type_qs.id, created_by=request_user, nid_number= nid_number, passport_number = passport_number
        )
        else:
            employee_information_qs = employee_information_qs.update(
                name=name,
                image=image,  phone_number = phone, 
                user_id=qs.id, employee_company_id = company_qs.id, designations_id = designation_qs.id, employee_type_id = employee_type_qs.id, created_by=request_user, nid_number= nid_number, passport_number = passport_number
        )
            
            count +=1 
        
    return True


def multiple_department_create(department_list, request_user):
    for item in department_list:
        name = item.get('name')
        slug = item.get('slug')
        department_head = item.get('department_head')
        designation_list = item.get('designation_list')
        
        qs = Department.objects.filter(slug = slug).last()
        fk_qs = UserAccount.objects.filter(email = department_head).last()
        
        if qs:
            qs.name =name
            qs.slug =slug
            qs.save()
        else:
            qs = Department.objects.create(
                name = name, slug = slug, created_by = request_user
            )
            
        if fk_qs:
            qs.department_head_id  = fk_qs.id
            qs.save()
            
        if designation_list:
            department_qs = qs
            
            for new_item in designation_list:
                name = new_item.get('name')
                slug = new_item.get('slug')
                
                qs = Designation.objects.filter(slug = slug).last()
                if qs:
                    qs.name =name
                    qs.slug =slug
                    qs.departments_id =department_qs.id
                    qs.save()
                else:
                    qs = Designation.objects.create(
                        name = name, slug = slug, created_by = request_user, departments_id =department_qs.id
                    )
            
    return True

def multiple_user_permission_create(user_group_list, request_user):
    for item in user_group_list:
        group_name = item.get('group_name')
        custom_permission_list = item.get('custom_permission_list')
        print(f'................{group_name}......................') 
        
        qs = UserGroup.objects.filter(name__icontains = group_name).last()
        
        if qs:
            print(f"Update = {group_name}")
            qs.name =group_name
            qs.save()
        if not qs:
            print(f"Create = {group_name}")
            
            qs = UserGroup.objects.create(name=group_name
            )
            
        for permission in custom_permission_list:
            name = permission.get('name')
            f_qs = CustomPermission.objects.filter(name=name).first()
            if not f_qs:
                codename = name.lower().replace(" ", "_")   
                f_qs = CustomPermission.objects.create(
                    name=name,
                    codename=codename,
                    )
                
            f_qs = CustomPermission.objects.filter(name=name).last()
            
            qs.custom_permission.add(f_qs)
            
    return True
