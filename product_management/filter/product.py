import django_filters
from product_management.models import *
from django_filters.rest_framework import FilterSet
from django.db.models import Count, Min, Q
from datetime import date, datetime, timedelta
from django.utils import timezone
from datetime import datetime


class ProductAttributeFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(label="search",
                                         method="filter_model")
    is_active = django_filters.CharFilter(label="is_active",
                                         method="filter_model")

    class Meta:
        model = ProductAttribute
        fields = (
            'search',
            'is_active',
            )

    def filter_model(self, queryset, name, value):
        search = self.data.get('search')
        is_active = self.data.get('is_active')
        
        if search:
            queryset = queryset.filter(
                Q(name__icontains = search)
                | Q(slug__icontains = search)
                
            )
            
        if is_active:
            if is_active.lower() == 'true' :
                queryset = queryset.filter(
                    is_active = True 
                )
            else:
                queryset = queryset.filter(
                    is_active = False 
                )
                
        return queryset
   
   
class ProductAttributeValueFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(label="search",
                                         method="filter_model")
    is_active = django_filters.CharFilter(label="is_active",
                                         method="filter_model")

    class Meta:
        model = ProductAttributeValue
        fields = (
            'search',
            'is_active',
            )

    def filter_model(self, queryset, name, value):
        search = self.data.get('search')
        is_active = self.data.get('is_active')
        
        if search:
            queryset = queryset.filter(
                Q(name__icontains = search)
                | Q(slug__icontains = search)
                
            )
            
        if is_active:
            if is_active.lower() == 'true' :
                queryset = queryset.filter(
                    is_active = True 
                )
            else:
                queryset = queryset.filter(
                    is_active = False 
                )
                
        return queryset
   

class ProductFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(label="search",
                                         method="filter_model")
    shop = django_filters.CharFilter(label="shop",
                                         method="filter_model")
    category = django_filters.CharFilter(label="category",
                                         method="filter_model")
    group_slug = django_filters.CharFilter(label="group_slug",
                                         method="filter_model")
    sub_category = django_filters.CharFilter(label="sub_category",
                                         method="filter_model")
    status = django_filters.CharFilter(label="status",
                                         method="filter_model")
    brand = django_filters.CharFilter(label="brand",
                                         method="filter_model")
    supplier = django_filters.CharFilter(label="supplier",
                                         method="filter_model")
    is_gift_product = django_filters.CharFilter(label="is_gift_product",
                                         method="filter_model")
    is_top_sale = django_filters.CharFilter(label="is_top_sale",
                                         method="filter_model")
    is_out_of_stock = django_filters.CharFilter(label="is_out_of_stock",
                                         method="filter_model")
    is_special_day = django_filters.CharFilter(label="is_special_day",
                                         method="filter_model")
    is_new_arrival = django_filters.CharFilter(label="is_new_arrival",
                                         method="filter_model")
    is_active = django_filters.CharFilter(label="is_active",
                                         method="filter_model")
    min_price = django_filters.CharFilter(label="min_price",
                                         method="filter_model")
    max_price = django_filters.CharFilter(label="max_price",
                                         method="filter_model")
    max_price = django_filters.CharFilter(label="max_price",
                                         method="filter_model")
    campaign = django_filters.CharFilter(label="campaign",
                                         method="filter_model")

    class Meta:
        model = Product
        fields = (
            'search',
            'shop',
            'status',
            'group_slug',
            'category',
            'sub_category',
            'brand',
            'supplier',
            'is_gift_product',
            'is_top_sale',
            'is_out_of_stock',
            'is_special_day',
            'is_new_arrival',
            'is_active',
            'min_price',
            'max_price',
            'campaign',
            )

    def filter_model(self, queryset, name, value):
        search = self.data.get('search')
        shop = self.data.get('shop')
        status = self.data.get('status')
        group_slug = self.data.get('group_slug')
        category = self.data.get('category')
        sub_category = self.data.get('sub_category')
        brand = self.data.get('brand')
        supplier = self.data.get('supplier')
        is_gift_product = self.data.get('is_gift_product')
        is_out_of_stock = self.data.get('is_out_of_stock')
        is_top_sale = self.data.get('is_top_sale')
        is_special_day = self.data.get('is_special_day')
        is_new_arrival = self.data.get('is_new_arrival')
        is_active = self.data.get('is_active')
        min_price = self.data.get('max_price')
        max_price = self.data.get('min_price')
        campaign = self.data.get('campaign')
        
        if search:
            queryset = queryset.filter(
                Q(name__icontains = search)
                | Q(slug__icontains = search)
                | Q(product_code__icontains = search)
                | Q(product_parent__name__icontains = search)
                | Q(product_parent__slug__icontains = search)
                | Q(gift_product__name__icontains = search)
                | Q(gift_product__slug__icontains = search)
                | Q(product_price_infos__product_stocks__barcode__icontains = search)
                
            )
        if group_slug:
            queryset = queryset.filter(
                Q(category__category_group__name__icontains = group_slug)
                | Q(category__category_group__slug__icontains = group_slug)
            )
            
        if category:
            #TODO after all data add properly then enable this code
            
            queryset = queryset.filter(
                Q(category__name__icontains = category)
                | Q(category__slug__icontains = category)
            )
        
        if shop:
            queryset = queryset.filter(
                Q(product_price_infos__product_stocks__stock_location__name__icontains = shop)
                | Q(product_price_infos__product_stocks__stock_location__slug__icontains = shop)
            )
            
        if status:
            queryset = queryset.filter(
                Q(status = status)
            )
            
        if campaign: 
            queryset = queryset.filter(
                product_price_infos__discount__slug = campaign,
            )
            
        if min_price and max_price: 
            queryset = queryset.filter(
                product_price_infos__mrp__gte = float(min_price),
                product_price_infos__mrp__lte = float(max_price)
            )
            
        if sub_category:
            queryset = queryset.filter(
                Q(sub_category__name__icontains = sub_category)
                | Q(sub_category__slug__icontains = sub_category)
                
            )
            
        if brand:
            queryset = queryset.filter(
                Q(brand__name__icontains = brand)
                | Q(brand__slug__icontains = brand)
            )
        if supplier:
            queryset = queryset.filter(
                Q(supplier__name__icontains = supplier)
                | Q(supplier__slug__icontains = supplier)
            )
            
        if is_gift_product:
            if is_gift_product.lower() == 'true' :
                queryset = queryset.filter(
                    is_gift_product = True 
                )
            else:
                queryset = queryset.filter(
                    is_gift_product = False 
                )
            
        if is_out_of_stock:
            if is_out_of_stock.lower() == 'true' :
                queryset = queryset.filter(
                    Q(is_out_of_stock = True)
                    |Q(is_cart_disabled = False) 
                )
            else:
                queryset = queryset.filter(
                    Q(is_out_of_stock = False) 
                    |Q(is_cart_disabled = True) 
                )
            
        if is_top_sale:
            if is_top_sale.lower() == 'true' :
                queryset = queryset.filter(
                    is_top_sale = True 
                )
            else:
                queryset = queryset.filter(
                    is_top_sale = False 
                )
            
        if is_special_day:
            if is_special_day.lower() == 'true' :
                queryset = queryset.filter(
                    is_special_day = True 
                )
            else:
                queryset = queryset.filter(
                    is_special_day = False 
                )
            
        if is_new_arrival:
            if is_new_arrival.lower() == 'true' :
                queryset = queryset.filter(
                    is_new_arrival = True 
                )
            else:
                queryset = queryset.filter(
                    is_new_arrival = False 
                )
            
        if is_active:
            if is_active.lower() == 'true' :
                queryset = queryset.filter(
                    is_active = True 
                )
            else:
                queryset = queryset.filter(
                    is_active = False 
                )
                
        queryset = queryset.distinct()
        
        return queryset
   
   
   
class ShopWiseProductFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(label="search",
                                         method="filter_model")
    shop = django_filters.CharFilter(label="category",
                                         method="filter_model")
    brand = django_filters.CharFilter(label="brand",
                                         method="filter_model")
    supplier = django_filters.CharFilter(label="supplier",
                                         method="filter_model")
    is_gift_product = django_filters.CharFilter(label="is_gift_product",
                                         method="filter_model")
    is_top_sale = django_filters.CharFilter(label="is_top_sale",
                                         method="filter_model")
    is_out_of_stock = django_filters.CharFilter(label="is_out_of_stock",
                                         method="filter_model")
    is_special_day = django_filters.CharFilter(label="is_special_day",
                                         method="filter_model")
    is_active = django_filters.CharFilter(label="is_active",
                                         method="filter_model")

    class Meta:
        model = Product
        fields = (
            'search',
            'shop',
            'brand',
            'supplier',
            'is_gift_product',
            'is_top_sale',
            'is_out_of_stock',
            'is_special_day',
            'is_active',
            )

    def filter_model(self, queryset, name, value):
        search = self.data.get('search')
        shop = self.data.get('shop')
        brand = self.data.get('brand')
        supplier = self.data.get('supplier')
        is_gift_product = self.data.get('is_gift_product')
        is_out_of_stock = self.data.get('is_out_of_stock')
        is_top_sale = self.data.get('is_top_sale')
        is_special_day = self.data.get('is_special_day')
        is_active = self.data.get('is_active')
        
        if search:
            queryset = queryset.filter(
                Q(name__icontains = search)
                | Q(slug__icontains = search)
                | Q(product_code__icontains = search)
                | Q(product_parent__name__icontains = search)
                | Q(product_parent__slug__icontains = search)
                | Q(gift_product__name__icontains = search)
                | Q(gift_product__slug__icontains = search)
                | Q(product_price_infos__product_stocks__barcode__icontains = search)
                
            ).distinct() 
            
        if brand:
            queryset = queryset.filter(
                Q(brand__name__icontains = brand)
                | Q(brand__slug__icontains = brand)
            )
        if supplier:
            queryset = queryset.filter(
                Q(supplier__name__icontains = supplier)
                | Q(supplier__slug__icontains = supplier)
            )
            
        if is_gift_product:
            if is_gift_product.lower() == 'true' :
                queryset = queryset.filter(
                    is_gift_product = True 
                )
            else:
                queryset = queryset.filter(
                    is_gift_product = False 
                )
            
        if is_out_of_stock:
            if is_out_of_stock.lower() == 'true' :
                queryset = queryset.filter(
                    is_out_of_stock = True 
                )
            else:
                queryset = queryset.filter(
                    is_out_of_stock = False 
                )
            
        if is_top_sale:
            if is_top_sale.lower() == 'true' :
                queryset = queryset.filter(
                    is_top_sale = True 
                )
            else:
                queryset = queryset.filter(
                    is_top_sale = False 
                )
            
        if is_special_day:
            if is_special_day.lower() == 'true' :
                queryset = queryset.filter(
                    is_special_day = True 
                )
            else:
                queryset = queryset.filter(
                    is_special_day = False 
                )
            
        if is_active:
            if is_active.lower() == 'true' :
                queryset = queryset.filter(
                    is_active = True 
                )
            else:
                queryset = queryset.filter(
                    is_active = False 
                )
                
        return queryset
   
    
class ProductStockFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(label="search",
                                         method="filter_model")
    # category = django_filters.CharFilter(label="category",
    #                                      method="filter_model")
    # sub_category = django_filters.CharFilter(label="sub_category",
    #                                      method="filter_model")
    stock_location = django_filters.CharFilter(label="location",
                                         method="filter_model")
    status = django_filters.CharFilter(label="status",
                                         method="filter_model")
    stock_in_start_date = django_filters.CharFilter(label="start_date",
                                         method="filter_model")
    stock_in_end_date = django_filters.CharFilter(label="end_date",
                                         method="filter_model")
    brand = django_filters.CharFilter(label="brand",
                                         method="filter_model")
    supplier = django_filters.CharFilter(label="supplier",
                                         method="filter_model")
    seller = django_filters.CharFilter(label="Seller",
                                         method="filter_model")

    class Meta:
        model = ProductStock
        fields = (
            'search',
            # 'category',
            # 'sub_category',
            'stock_location',
            'stock_in_start_date',
            'stock_in_end_date',
            'status',
            'brand',
            'supplier',
            )

    def filter_model(self, queryset, name, value):
        search = self.data.get('search')
        category = self.data.get('category')
        sub_category = self.data.get('sub_category')
        location = self.data.get('location')
        stock_in_start_date = self.data.get('stock_in_start_date')
        stock_in_end_date = self.data.get('stock_in_end_date')
        status = self.data.get('status')
        brand = self.data.get('brand')
        supplier = self.data.get('supplier')
        
        if search:
            queryset = queryset.filter(
                Q(barcode__icontains = search)
                | Q(product_price_info__product__product_code__icontains = search)
                | Q(product_price_info__product__name__icontains = search)
                | Q(product_price_info__product__slug__icontains = search)
                
            )
        if location:
            queryset = queryset.filter(
                Q(stock_location__name__icontains = location)
                | Q(stock_location__slug__icontains = location)
                
            )
        if status:
            queryset = queryset.filter(
                Q(status = status)
            )
            
        if stock_in_start_date and stock_in_end_date:
            queryset = queryset.filter(
                stock_in_date__date__range=(stock_in_start_date, stock_in_end_date)
            )
            
        if category:
            queryset = queryset.filter(
                Q(product_price_info__product__category__name__icontains = category)
                |Q(product_price_info__product__category__name__icontains = category)
            )
            
        if sub_category:
            queryset = queryset.filter(
                Q(product_price_info__product__sub_category__name__icontains = sub_category)
                |Q(product_price_info__product__sub_category__slug__icontains = sub_category)
            )
            
        if brand:
            queryset = queryset.filter(
                Q(product_price_info__product__brand__name__icontains = brand)
                |Q(product_price_info__product__brand__slug__icontains = brand)
            )
            
        if supplier:
            queryset = queryset.filter(
                Q(product_price_info__product__supplier__name__icontains = supplier)
                |Q(product_price_info__product__supplier__slug__icontains = supplier)
            )
        return queryset
    

class ProductStockLogFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(label="search",
                                         method="filter_model")
    stock_location = django_filters.CharFilter(label="location",
                                         method="filter_model")
    start_date = django_filters.CharFilter(label="start_date",
                                         method="filter_model")
    end_date = django_filters.CharFilter(label="end_date",
                                         method="filter_model")
    status = django_filters.CharFilter(label="status",
                                         method="filter_model")

    class Meta:
        model = ProductStockLog
        fields = (
            'search',
            'stock_location',
            )

    def filter_model(self, queryset, name, value):
            search = self.data.get('search')
            stock_location = self.data.get('location')
            stock_in_date = self.data.get('in_date')


class ProductStockTransferFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(label="search",
                                         method="filter_model")
    status = django_filters.CharFilter(label="status",
                                         method="filter_model")
    stock_transfer_type = django_filters.CharFilter(label="stock_transfer_type",
                                         method="filter_model")
    from_shop = django_filters.CharFilter(label="from_shop",
                                         method="filter_model")
    to_shop = django_filters.CharFilter(label="to_shop",
                                         method="filter_model")
    start_date = django_filters.CharFilter(label="start_date",
                                         method="filter_model")
    end_date = django_filters.CharFilter(label="end_date",
                                         method="filter_model")

    class Meta:
        model = ProductStockTransfer
        fields = (
            'search',
            'status',
            'stock_transfer_type',
            'from_shop',
            'to_shop',
            'start_date',
            'end_date',
            )

    def filter_model(self, queryset, name, value):
        search = self.data.get('search')
        status = self.data.get('status')
        stock_transfer_type = self.data.get('stock_transfer_type')
        from_shop = self.data.get('from_shop')
        to_shop = self.data.get('to_shop')
        start_date = self.data.get('start_date')
        end_date = self.data.get('end_date')
        
        if search:
            queryset = queryset.filter(
                Q(requisition_no__icontains = search)
                | Q(product_stock__barcode__icontains = search)
            )
            
        if status:
            queryset = queryset.filter(
                Q(status = status)
            )
            
        if stock_transfer_type:
            queryset = queryset.filter(
                Q(stock_transfer_type = stock_transfer_type)
            )
            
        if from_shop:
            queryset = queryset.filter(
                Q(from_shop__name__icontains = from_shop)
                | Q(from_shop__slug__icontains = from_shop)
            )
            
        if to_shop:
            queryset = queryset.filter(
                Q(to_shop__name__icontains = to_shop)
                | Q(to_shop__slug__icontains = to_shop)
            )
            
        if start_date and end_date:
            queryset = queryset.filter(
                created_at__date__range = (start_date, end_date)
            )
            
        queryset = queryset.distinct()
            
        return queryset
   
    
    

class ShopWiseZeroStockLogFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(label="search",
                                         method="filter_model")
    office_location = django_filters.CharFilter(label="office_location",
                                         method="filter_model")
    product = django_filters.CharFilter(label="product",
                                         method="filter_model")
    start_date = django_filters.CharFilter(label="start_date",
                                         method="filter_model")
    end_date = django_filters.CharFilter(label="end_date",
                                         method="filter_model")

    class Meta:
        model = ShopWiseZeroStockLog
        fields = (
            'search',
            'office_location',
            'product', 
            'start_date', 
            'end_date', 
            )

    def filter_model(self, queryset, name, value):
        search = self.data.get('search')
        office_location = self.data.get('office_location')
        product = self.data.get('product') 
        start_date = self.data.get('start_date') 
        end_date = self.data.get('end_date') 
        
        if search:
            queryset = queryset.filter(
                Q(office_location__name__icontains = search)
                | Q(office_location__slug__icontains = search)
                | Q(product__slug__icontains = search)
                | Q(product__slug__icontains = search)
            )
            
        if office_location:
            queryset = queryset.filter(
                Q(office_location__name__icontains = office_location)
                | Q(office_location__slug__icontains = office_location)
            ) 
            
        if product:
            queryset = queryset.filter(
                Q(product__name__icontains = product)
                | Q(product__slug__icontains = product)
            ) 
            
        if start_date and end_date:
            queryset = queryset.filter(
                zero_stock_date__date__range = (start_date, end_date)
            ) 
            
        return queryset
   
   