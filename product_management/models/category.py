from django.db import models
from user.models import UserAccount
from base.models import Company
from django.utils.translation import gettext_lazy as _
from discount.models import Discount

# Create your models here.

class CategoryGroup(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255,unique=True)
    translation = models.JSONField(default=dict, blank=True, null=True)
    is_featured = models.BooleanField(default=True)
    is_show_in_ecommece = models.BooleanField(default=True)
    is_show_in_pos = models.BooleanField(default=True)
    ordering = models.PositiveIntegerField(default=0)
    
    company = models.ForeignKey(
        Company, on_delete=models.SET_NULL,  related_name='category_groups',
        null=True, blank=True)
    
    is_active = models.BooleanField(default=True)
    remarks = models.TextField(null=True, blank=True)
#     """ For SEO Friendly for Operations """
    
    meta_title = models.CharField(max_length=200)
    meta_description = models.TextField(null=True, blank=True)
    canonical = models.URLField(null=True, blank=True)
    banner_image = models.TextField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    created_by = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE ,related_name='category_group_created_bys')
    updated_by = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE,  related_name='category_group_updated_bys',
        null=True, blank=True)
    
    def __str__(self):
        return self.name
    class Meta:
        ordering = ["-id"]
        
        

class Category(models.Model):
    STRUCTURECHOICES=[
        ("STANDALONE", "Stand Alone"),
        ("PARENT", "Parent"),
        ("CHILD", "Child"),
        ("CHILD_OF_CHILD", "Child of Child"),
    ]
    name = models.CharField(max_length=255)
    translation = models.JSONField(default=dict, blank=True, null=True)
    category_group = models.ForeignKey(CategoryGroup,
                                      on_delete=models.SET_NULL, blank=True, null=True, 
                                      related_name='categories')
    category_parent = models.ForeignKey('self',
                                on_delete=models.SET_NULL,
                                null=True, blank=True,
                                related_name='categories',
                                help_text=_("Only choose a PARENT Category if you're creating a child "
                                "category.  For example if this is PC "
                                "3 of a particular [Normal, Gaming].  Leave blank if this is a "
                                "stand-alone Category (i.e. there is only one version of"
                                " this category).")
                    )
    slug = models.SlugField(max_length=255, unique=True)
    image = models.URLField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    
    # FOR PC Builder Category Start ***
    is_for_pc_builder = models.BooleanField(default=False)
    is_required_for_pc_builder = models.BooleanField(default=False)
    # FOR PC Builder Category END ***
    
    show_in_ecommerce = models.BooleanField(default=True)
    ordering = models.PositiveIntegerField(default=0) 
    featured_ordering = models.PositiveIntegerField(default=0) 
    status = models.CharField(max_length=30, choices=STRUCTURECHOICES) # Auto Generated
    remarks = models.TextField(null=True, blank=True)
    # ......***...... Note : Hide Because of Status Add ......***......
    
    # has_child = models.BooleanField(default=False) 

    """ For SEO Friendly for Operations """
    meta_title = models.CharField(max_length=200,null=True, blank=True)
    meta_description = models.TextField(null=True, blank=True)
    canonical = models.URLField(null=True, blank=True)
    banner_image = models.TextField(null=True, blank=True)
    
    discount = models.ForeignKey(Discount,
                                on_delete=models.SET_NULL, blank=True, null=True,
                                related_name='categories')
    
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    created_by = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE ,related_name='category_created_bys')
    updated_by = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE,  related_name='category_updated_bys',
        null=True, blank=True)

    def __str__(self):
        return self.name
    
     # ....***.... For Status Automatically Setup  ....***....

    def generate_category_status(self):
        status = 'STANDALONE'
        category_parent = None

        category_parent_status = None

        if self.category_parent:
            category_parent_status = self.category_parent.status

        category_parent_parent_id = None
        
        if self.status == 'STANDALONE' and self.category_parent:
            category_parent = None
            # category_parent_status = 'PARENT'
            # category_parent_parent_id = None
            # status = 'CHILD'
            # category_parent = self.category_parent
            

        elif self.status == 'PARENT' and self.category_parent:
            category_parent = None
            category_parent = None

        elif self.status == 'CHILD' and not self.category_parent:
            status = 'STANDALONE'
        
        
        elif self.status == 'CHILD' and self.category_parent:
            category_parent_status = 'PARENT'
            category_parent_parent_id = None
            status = 'CHILD'
            category_parent = self.category_parent
            
        if self.category_parent:
            if self.category_parent.status == 'CHILD' and self.category_parent:
                category_parent_status = 'CHILD'
                category_parent_parent_id = self.category_parent.id
                status = 'CHILD_OF_CHILD'
                category_parent = self.category_parent


        return {
            "status": status,
            'category_parent': category_parent,
            'category_parent_status': category_parent_status,
            'category_parent_parent_id': category_parent_parent_id,
        }

    # def save(self, *args, **kwargs):
    #     if not self == self.category_parent:
    #         obj = self.generate_category_status()
    #         self.status = obj.get('status')
    #         self.category_parent = obj.get('category_parent')

    #         if obj.get('category_parent'):
    #             self.category_parent.status = obj.get('category_parent_status')
    #             self.category_parent.category_parent = obj.get('category_parent_parent_id')

    #         if obj.get('status') == 'CHILD' and obj.get('category_parent'):
    #             self.is_child = True
    #             self.product_group = None
    #         else:
    #             self.is_child = False

    #         super().save(*args, **kwargs)
    #     pass