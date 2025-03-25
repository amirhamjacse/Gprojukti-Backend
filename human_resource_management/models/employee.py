from django.db import models

from django.utils.translation import gettext_lazy as _
from user.models import UserAccount
from django.utils.timezone import timedelta

from django.utils.translation import gettext_lazy as _
from utils.helpers import (
    time_str_mix_slug)
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models.signals import post_save, pre_save
from django.utils.text import slugify
from base.models import DAYS, Company
from location.models import Area, OfficeLocation, POSArea, POSRegion
from utils.generates import unique_slug_generator

# Create your models here.

class EmployeeDivision(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255,unique=True)
    division_head = models.ForeignKey(
        UserAccount, on_delete=models.SET_NULL,  related_name='employee_divisions',
        null=True, blank=True)
    is_active = models.BooleanField(default=True)
    remarks = models.TextField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    created_by = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE ,related_name='employee_division_created_bys')
    updated_by = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE,  related_name='employee_division_updated_bys',
        null=True, blank=True)
    
    def __str__(self):
        return self.name
    class Meta:
        ordering = ["-id"]
        
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slug_generator(self.name)
        super().save(*args, **kwargs)

class Department(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255,unique=True)
    is_active = models.BooleanField(default=True)
    employee_division = models.ForeignKey(
        EmployeeDivision, on_delete=models.SET_NULL,  related_name='departments',
        null=True, blank=True)
    department_head = models.ForeignKey(
        UserAccount, on_delete=models.SET_NULL,  related_name='departments',
        null=True, blank=True)
    employee_need = models.PositiveBigIntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    created_by = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE ,related_name='department_created_bys')
    updated_by = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE,  related_name='department_updated_bys',
        null=True, blank=True)
    
    def __str__(self):
        return self.name
    class Meta:
        ordering = ["-id"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slug_generator(self.name)
        super().save(*args, **kwargs)

class Grading(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255,unique=True)
    is_active = models.BooleanField(default=True)  
    remarks = models.TextField(null=True, blank=True) 
    
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    created_by = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE ,related_name='grading_created_bys')
    updated_by = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE,  related_name='grading_updated_bys',
        null=True, blank=True)
    
    def __str__(self):
        return self.name
    class Meta:
        ordering = ["-id"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slug_generator(self.name)
        super().save(*args, **kwargs)     
        
class Ranking(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255,unique=True)
    grade = models.ForeignKey(
        Grading, on_delete=models.SET_NULL,  related_name='rankings',
        null=True, blank=True)
    is_active = models.BooleanField(default=True) 
    remarks = models.TextField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    created_by = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE ,related_name='ranking_created_s')
    updated_by = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE,  related_name='ranking_updated_bys',
        null=True, blank=True)
    
    def __str__(self):
        return self.name
    class Meta:
        ordering = ["-id"]
        
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slug_generator(self.name)
        super().save(*args, **kwargs)     
        
class Designation(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255,unique=True)
    is_active = models.BooleanField(default=True)
    remarks = models.TextField(null=True, blank=True)
    departments = models.ForeignKey(
        Department, on_delete=models.SET_NULL,  related_name='designations',
        null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    created_by = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE ,related_name='designation_created_bys')
    updated_by = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE,  related_name='designation_updated_bys',
        null=True, blank=True)
    
    def __str__(self):
        return self.name
    class Meta:
        ordering = ["-id"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slug_generator(self.name)
        super().save(*args, **kwargs)    
             
class EmployeeType(models.Model):
    name = models.CharField(max_length=255) # Full Time, Part-Time, Probation
    slug = models.SlugField(max_length=555, unique=True)
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    created_by = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE ,related_name='employee_type_created_bys')
    updated_by = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE,  related_name='employee_type_updated_bys',
        null=True, blank=True)
    
    def __str__(self):
        return self.name
    class Meta:
        ordering = ["-id"]
    
class EmployeeGuardianInformation(models.Model):
    RELATIONSHIP_TYPE = [
        ('FATHER', 'Father'),
        ('MOTHER', 'Mother'),
        ('SISTER', 'Sister'),
        ('BROTHER', 'Brother'),
        ('HUSBAND', 'Husband'),
        ('WIFE', 'Wife'),
        ('OTHERS', 'Others'),
    ]
    name = models.CharField(max_length=150)
    slug = models.SlugField(max_length=255,unique=True)
    occupation = models.CharField(max_length=250, blank=True)
    phone_number = models.CharField(max_length=50, blank=True, null=True)
    nid_number = models.CharField(max_length=150, blank=True, null=True)
    passport_number = models.CharField(max_length=150, blank=True, null=True)
    relationship_type = models.CharField(
        choices=RELATIONSHIP_TYPE, max_length=50, default="FATHER"
        )
    remarks = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    created_by = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE ,related_name='employee_guardian_information_created_bys')
    updated_by = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE,  related_name='employee_guardian_information_updated_bys',
        null=True, blank=True)
    
    def __str__(self):
        return self.name
    class Meta:
        ordering = ["-id"]
    
class EmployeeAddressInformation(models.Model):
    ADDRESS_TYPE = [
        ('PERMANENT', 'Permanent'),
        ('PRESENT', 'Present'),
        ('OTHERS', 'Others'),
    ]
    full_address = models.CharField(max_length=550)
    city = models.CharField(max_length=250, blank=True)
    area_name = models.ForeignKey(
        Area, on_delete=models.SET_NULL, blank=True, null=True,
        related_name='employee_address_informations')
    district_name = models.CharField(max_length=250, null = True, blank=True)
    division_name = models.CharField(max_length=250, null = True, blank=True)
    country_name = models.CharField(max_length=250, null = True, blank=True)
    address_type = models.CharField(
        choices=ADDRESS_TYPE, max_length=50, default="PERMANENT")
    remarks = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    created_by = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE ,related_name='employee_address_information_created_bys')
    updated_by = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE,  related_name='employee_address_information_updated_bys',
        null=True, blank=True)
    
    def __str__(self):
        return f"{(self.full_address)} and {str(self.id)}"
    
    class Meta:
        ordering = ["-id"]
    
class ExamType(models.Model):
    name = models.CharField(max_length=550)
    slug = models.SlugField(max_length=255,unique=True)
    remarks = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    created_by = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE ,related_name='exam_type_created_bys')
    updated_by = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE,  related_name='exam_type_updated_bys',
        null=True, blank=True)
    
    def __str__(self):
        return str(self.name)
    
    class Meta:
        ordering = ["-id"]
    
class EmployeeEducationInformation(models.Model):
    exam_type = models.ForeignKey(
        ExamType, on_delete=models.SET_NULL,
        related_name='employee_education_informations',
        null=True, blank=True)
    institution_name = models.CharField(max_length=355)
    slug = models.SlugField(max_length=255,unique=True)
    board_name = models.CharField(max_length=355, null=True, blank=None)
    grade = models.CharField(max_length=355, null=True, blank=None)
    file = models.TextField(blank=True, null=True)
    remarks = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    created_by = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE ,related_name='employee_education_information_created_bys')
    updated_by = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE,  related_name='employee_education_information_updated_bys',
        null=True, blank=True)
    
    def __str__(self):
        return f"Institution Name = {self.institution_name} and Exam Type = {self.exam_type.name}"
    
    class Meta:
        ordering = ["-id"]
    
class JobExperienceInformation(models.Model):
    company_name = models.CharField(max_length=355)
    slug = models.SlugField(max_length=255,unique=True)
    address = models.TextField(null=True, blank=None)
    website_url = models.URLField(null=True, blank=None)
    joining_date = models.DateField(null = True, blank = True)
    resign_date = models.DateField(null = True, blank = True)
    total_job_experience = models.CharField(max_length=355,null = True, blank = True)
    remarks = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    created_by = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE ,related_name='job_experience_information_created_bys')
    updated_by = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE,  related_name='job_experience_information_updated_bys',
        null=True, blank=True)
    
    def __str__(self):
        return str(self.company_name)
    
    class Meta:
        ordering = ["-id"]
    
class BankInformation(models.Model):
    account_name = models.CharField(max_length=355)
    slug = models.SlugField(max_length=255,unique=True)
    account_number = models.CharField(max_length=355, null=True, blank=None)
    bank_name = models.CharField(max_length=355, null=True, blank=None)
    branch_name = models.CharField(max_length=355, null=True, blank=None)
    routing_number = models.CharField(max_length=355, null=True, blank=None)
    expire_date = models.CharField(max_length=355, null=True, blank=None)
    remarks = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    created_by = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE ,related_name='bank_information_created_bys')
    updated_by = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE,  related_name='bank_information_updated_bys',
        null=True, blank=True)
    
    def __str__(self):
        return str(self.account_name)
    
    class Meta:
        ordering = ["-id"]
    
    
class EmployeeInformation(models.Model):
    user = models.OneToOneField(
        UserAccount, on_delete=models.SET_NULL, blank=True, null=True,
        related_name="employee_informations"
    )
    employee_id = models.CharField(max_length=355,unique=True)
    image = models.TextField(null=True, blank=True)
    name = models.CharField(max_length=355,blank=True, null=True)
    slug = models.SlugField(max_length=555, unique=True)
    nid_number = models.CharField(max_length=355,blank=True, null=True)
    passport_number = models.CharField(max_length=355,blank=True, null=True)
    phone_number = models.CharField(max_length=355,blank=True, null=True)
    reporting_person = models.ForeignKey(
        'self', on_delete=models.SET_NULL,
        related_name='employee_informations',
        null=True, blank=True)
    employee_company = models.ForeignKey(
        Company, on_delete=models.SET_NULL,
        related_name='employee_informations',
        null=True, blank=True)
    employee_type = models.ForeignKey(
        EmployeeType, on_delete=models.SET_NULL,
        related_name='employee_informations',
        null=True, blank=True)
    designations = models.ForeignKey(
        Designation, on_delete=models.SET_NULL,
        related_name='employee_informations',
        null=True, blank=True)
    pos_area = models.ForeignKey(
        POSArea, on_delete=models.SET_NULL,
        related_name='employee_informations',
        null=True, blank=True)
    pos_reason = models.ForeignKey(
        POSRegion, on_delete=models.SET_NULL,
        related_name='employee_informations',
        null=True, blank=True)
    work_station = models.ForeignKey(
        OfficeLocation, on_delete=models.SET_NULL,
        related_name='employee_informations',
        null=True, blank=True)
    rank = models.ForeignKey(
        Ranking, on_delete=models.SET_NULL,
        related_name='employee_informations',
        null=True, blank=True)
    guardian_information = models.ManyToManyField(
        to=EmployeeGuardianInformation,blank=True,
        related_name='employee_informations'
        )
    employee_address_information = models.ManyToManyField(
        to=EmployeeAddressInformation,blank=True,
        related_name='employee_informations'
        )
    employee_education_information = models.ManyToManyField(
        to=EmployeeEducationInformation,blank=True,
        related_name='employee_informations'
        )
    job_experience_information = models.ManyToManyField(
        to=JobExperienceInformation,blank=True,
        related_name='employee_informations'
        )
    bank_information = models.ManyToManyField(
        to=BankInformation,blank=True,
        related_name='employee_informations'
        )
    joining_date = models.DateField(blank=True, null=True)
    next_confirmation_date = models.DateField(blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    resign_date = models.DateField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    created_by = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE ,related_name='employee_information_created_bys')
    updated_by = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE,  related_name='employee_information_updated_bys',
        null=True, blank=True)
    
    
    def __str__(self):
        return str(self.name)
    
    class Meta:
        ordering = ["-id"]

    
class EmployeeInformationLog(models.Model):
    employee_information = models.ForeignKey(
        EmployeeInformation, on_delete=models.SET_NULL, blank=True, null=True,  related_name='employee_information_logs')
    employee_type = models.ForeignKey(
        EmployeeType, on_delete=models.SET_NULL, blank=True, null=True,  related_name='employee_information_logs',)
    employee_designation = models.ForeignKey(
        Designation, on_delete=models.SET_NULL, blank=True, null=True,  related_name='employee_information_logs',)
    employee_rank = models.ForeignKey(
        Ranking, on_delete=models.SET_NULL, blank=True, null=True,  related_name='employee_information_logs',)
    confirmation_date = models.DateTimeField(blank=True, null=True)
    employee_info = models.JSONField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    created_by = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE ,related_name='employee_information_log_created_bys')
    updated_by = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE,  related_name='employee_information_log_bys',
        null=True, blank=True)
    
    def __str__(self):
        if self.employee_information:
            return str(self.employee_information.name)
        else:
            return str(self.id)
    