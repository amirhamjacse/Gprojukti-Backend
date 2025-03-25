from django.contrib.auth.base_user import BaseUserManager
from gporjukti_backend_v2.settings import TIME_ZONE
from django.db import models
from django.contrib.auth.models import AbstractUser, User, UserManager, Group, Permission
import uuid
from django.utils import timezone
from random import randint
from django.utils.timezone import timedelta

from django.utils.translation import gettext_lazy as _
from utils.helpers import (
    time_str_mix_slug)
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models.signals import post_save, pre_save
from django.utils.text import slugify


# Create your models here.

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        # if not username:
        #     raise ValueError('The given username must be set')
        # phone = self.normalize_email(phone)
        username = self.model.normalize_username(username)
        user = self.model(
            # username=username, email=email,
            **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username=None,  password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, password, **extra_fields)

    def create_superuser(self, username=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, password, **extra_fields)

class CustomPermission(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    codename = models.CharField(_('codename'), max_length=255)
    remarks = models.CharField(max_length=255, blank=True, null=True)
    model_name = models.CharField(max_length=255, blank=True, null=True)
    serial_no = models.CharField(max_length=10, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return str(self.name)
    
    class Meta:
        ordering = ["serial_no"]
        
class UserGroup(Group):
    custom_permission =  models.ManyToManyField(
        to=CustomPermission,blank=True, null=True,
        related_name='user_groups'
        )
    
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    
    def __str__(self):
        return str(self.id)
    
    class Meta:
        ordering = ["-id"]
    
class UserAccount(AbstractUser):
    username = None
    phone = None
    last_name = None
    
    first_name = models.CharField(_('first name'), max_length=150, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)
    email = models.EmailField(max_length=100, unique=True)
    phone = models.CharField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True)
    custom_permission = models.ManyToManyField(
        to=CustomPermission,blank=True,
        related_name='user_accounts'
        )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["phone"]
    objects = UserManager()
    
    def __str__(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        if self.email:
            return self.email
        elif self.phone:
            return self.phone
        else:
            return str(self.id)
        
    class Meta:
        ordering = ["-id"]

class UserType(models.Model):
    name = models.CharField(max_length=255) # Ex: Customer, Employee, Seller, Corporate Client
    slug = models.SlugField(max_length=555, unique=True)
    is_active = models.BooleanField(default=True)
    remarks = models.TextField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    created_by = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE ,related_name='user_type_created_bys')
    updated_by = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE,  related_name='user_type_updated_bys',
        null=True, blank=True)
    
    def __str__(self):
        return self.name
    class Meta:
        ordering = ["-id"]
 
class UserInformation(models.Model):
    user = models.OneToOneField(
        UserAccount, on_delete=models.SET_NULL, blank=True, null=True,
        related_name="user_informations"
    )
    name = models.CharField(max_length=355,blank=True, null=True)
    slug = models.SlugField(max_length=555, unique=True)
    address = models.TextField(null=True, blank=True)
    image = models.TextField(null=True, blank=True)
    user_type = models.ForeignKey(
        UserType, on_delete=models.SET_NULL,  related_name='user_informations',
        null=True, blank=True)
    remarks = models.TextField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    created_by = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE ,related_name='user_information_created_bys')
    updated_by = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE,  related_name='user_information_updated_bys',
        null=True, blank=True)
    
    def __str__(self):
        if self.name:
            return f"Name = {self.name} and User ID ="
            # return f"Name = {self.name} and User ID =  {self.user.id}"
        
        return str(self.id)
    
    class Meta:
        ordering = ["-id"]

    
# ............***............ User Information ............***............

def user_info_slug_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        title = slugify(instance.name.lower()[:17])
        slug_binding = title + '-' + time_str_mix_slug()
        instance.slug = slug_binding


pre_save.connect(user_info_slug_pre_save_receiver, sender=UserInformation)