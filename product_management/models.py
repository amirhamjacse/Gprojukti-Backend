# from django.db import models
# from base.models import BaseModel
# from django.core.exceptions import  ValidationError
# from django.utils.translation import gettext_lazy as _

# # Create your models here.

# class ProductGroup(models.Model):
#     name = models.CharField(max_length=255)
#     translation = models.JSONField(default=dict)
#     slug = models.SlugField(max_length=255, unique=True)
    
#     is_active = models.BooleanField(default=True)
#     is_featured = models.BooleanField(default=False)
#     is_show_in_ecommerce = models.BooleanField(default=True)
#     is_show_in_pos = models.BooleanField(default=True)
#     ordering = models.PositiveIntegerField(default=0)

#     """ For SEO Friendly for Operations """
    
#     metaTitle = models.CharField(max_length=200)
#     metaDescription = models.TextField(null=True, blank=True)
#     canonical = models.URLField()
#     banner_image = models.TextField(null=True, blank=True)

#     class Meta:
#         ordering = ['ordering']
#         indexes = [
#             models.Index(fields=['is_active']),
#             models.Index(fields=['is_featured']),
#             models.Index(fields=['ordering']),
#         ]

#     def __str__(self):
#         return str(self.name)

# class Category(models.Model):
#     STRUCTURECHOICES=[
#         ("STANDALONE", "Stand Alone"),
#         ("PARENT", "Parent"),
#         ("CHILD", "Child"),
#     ]
#     name = models.CharField(max_length=255)
#     translation = models.JSONField(default=dict)
#     product_group = models.ForeignKey(ProductGroup,
#                                       on_delete=models.SET_NULL, blank=True, null=True, 
#                                       related_name='categories',
#                                       null=True, blank=True)
#     category_parent = models.ForeignKey('self',
#                                 on_delete=models.SET_NULL, blank=True, null=True,
#                                 null=True, blank=True,
#                                 related_name='categories',
#                                 help_text=_("Only choose a parent Category if you're creating a child "
#                                 "category.  For example if this is PC "
#                                 "3 of a particular [Normal, Gaming].  Leave blank if this is a "
#                                 "stand-alone Category (i.e. there is only one version of"
#                                 " this category).")
#                     )
#     slug = models.SlugField(max_length=255, unique=True)
#     logo = models.URLField(null=True, blank=True)
#     description = models.TextField(null=True, blank=True)
#     is_active = models.BooleanField(default=True)
#     is_featured = models.BooleanField(default=False)
#     show_in_ecommerce = models.BooleanField(default=True)
#     ordering = models.PositiveIntegerField(default=0) 
#     featured_ordering = models.PositiveIntegerField(default=0) 
#     status = models.CharField(max_length=30, choices=STRUCTURECHOICES)
#     # ......***...... Note : Hide Because of Status Add ......***......
    
#     # has_child = models.BooleanField(default=False) 

#     """ For SEO Friendly for Operations """
#     metaTitle = models.CharField(max_length=200,null=True, blank=True)
#     metaDescription = models.TextField(null=True, blank=True)
#     canonical = models.URLField(null=True, blank=True)
#     banner_image = models.TextField(null=True, blank=True)
#     # discount = models.ForeignKey(Discount,
#     #                             on_delete=models.SET_NULL, blank=True, null=True,
#     #                             related_name='categories',
#     #                             null=True, blank=True)

#     class Meta:
#         ordering = ['ordering']
#         db_table = 'product_categories'
#         # indexes = [
#         #     models.Index(fields=['-created_at']),
#         #     models.Index(fields=['is_active']),
#         #     models.Index(fields=['is_featured']),
#         #     models.Index(fields=['ordering']),
#         #     models.Index(fields=['featured_ordering']),
#         # ]

#     def __str__(self):
#         return self.name
    
#     # ....***.... For Status Automatically Setup  ....***....


# # class ProductBrand(models.Model):
# #     name = models.CharField(max_length=255)
# #     slug = models.SlugField(max_length=300, unique=True)
# #     logo = models.URLField()
# #     is_active = models.BooleanField(default=True)
# #     is_featured = models.BooleanField(default=False)


# #     """ For SEO friendly Operations  """
# #     metaTitle = models.CharField(max_length=200)
# #     metaDescription = models.TextField(null=True, blank=True)
# #     canonical = models.URLField()

# #     class Meta:
# #         ordering = ['-created_at']
# #         db_table = 'product_brands'
# #         indexes = [
# #             models.Index(fields=['-created_at']),
# #             models.Index(fields=['is_active']),
# #             models.Index(fields=['is_featured']),
# #         ]

# #     def __str__(self):
# #         return self.name
    
# # class TaxCategory(models.Model):
# #     name = models.CharField(max_length=255)
# #     slug = models.SlugField(max_length=255, null=False, unique=True)
# #     value_in_percentage = models.FloatField()
# #     is_active = models.BooleanField(default=True)
# #     type = models.CharField(max_length=8, choices=TaxTypes.choices)

# #     class Meta:
# #         ordering = ['-created_at']
# #         db_table = 'tax_categories'
# #         indexes = [
# #             models.Index(fields=['-created_at']),
# #             models.Index(fields=['is_active']),
# #             models.Index(fields=['value_in_percentage']),
#         # ]

#     # def __str__(self):
#         # return self.name
