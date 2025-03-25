# from discount.models import *
# from discount.serializers import *
# from human_resource_management.models.employee import EmployeeInformation
# from product_management.models.category import Category
# from product_management.models.product import *
# from utils.actions import activity_log
# from utils.calculate import calculate_promo_code
# from utils.custom_veinlet import CustomViewSet
# from utils.generates import unique_slug_generator
# from utils.permissions import CheckCustomPermission
# from utils.response_wrapper import ResponseWrapper
# from utils.upload_image import image_upload
# from django.utils import timezone
# from discount.filters import *

# from django_filters.rest_framework import DjangoFilterBackend
# from rest_framework import permissions, viewsets, filters

# from rest_framework.permissions import AllowAny, IsAuthenticated

# class PublicDiscountViewSet(CustomViewSet):
#     queryset = Discount.objects.all()
#     lookup_field = 'pk'
#     serializer_class = DiscountSerializer
#     permission_classes = [AllowAny]
    
#     filter_backends = (
#         DjangoFilterBackend,
#         filters.OrderingFilter,
#     )
#     filterset_class = DiscountFilter
    
#     def get_serializer_class(self):
#         if self.action in ['create', 'update']:
#             self.serializer_class = DiscountSerializer
#         elif self.action in ['list']:
#             self.serializer_class = DiscountListSerializer
#         elif self.action in ['discount_add_in_product_or_category']:
#             self.serializer_class = productWiseDiscountPromoCodeAddSerializer
#         else:
#             self.serializer_class = DiscountDetailsSerializer

#         return self.serializer_class

#     # ..........***.......... Create ..........***..........
#     def create(self, request, *args, **kwargs):