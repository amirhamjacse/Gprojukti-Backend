from human_resource_management.models.employee import *
from location.models import *
from product_management.models.product import *
from user.models import *
from django.db.models import Q
from django.contrib.auth.hashers import make_password


def multiple_product_create(product_list, request_user):
    count = 31
    
    for item in product_list:
        name = item.get('name')
        # name = f"{item.get('name')}-{count}"
        status = item.get('status')
        short_description = item.get('short_description')
        minimum_stock_quantity = item.get('minimum_stock_quantity')
        product_code = item.get('product_code')
        # product_code = f"{item.get('product_code')}{count}"
        company = item.get('company')
        images = item.get('images')
        sku = f"{item.get('sku')}{count}"
        video_link = item.get('video_link')
        product_price_list = item.get('product_price_list')
        
        slug = unique_slug_generator(name=name)
        
        # product_qs = Product.objects.filter(name = name).last()
        product_qs = Product.objects.all().last()
        
        # product_qs = Product.objects.filter(name = name, slug = slug)
        
        company_qs = Company.objects.filter(id = 1).last()
        category_qs = Category.objects.all().order_by('?').last()
        brand_qs = Brand.objects.all().order_by('?').last()
        supplier_qs = Supplier.objects.all().order_by('?').last()
        selling_tax_category_qs = TaxCategory.objects.filter(type = 'SELL_TAX').order_by('?').last()
        buying_tax_category_qs = TaxCategory.objects.filter(type = 'BUY_TAX').order_by('?').last()
        discount_qs = Discount.objects.filter().order_by('?').last()
        promo_code_qs = PromoCode.objects.filter().order_by('?').last()
        
        
        if product_qs:
            product_qs = product_qs.update(
                name = name, status = status,
                short_description = short_description, description = short_description, minimum_stock_quantity = minimum_stock_quantity, 
                company = company_qs, images = images, brand = brand_qs,
                supplier = supplier_qs, selling_tax_category = selling_tax_category_qs, buying_tax_category = buying_tax_category_qs, video_link = video_link
            )
        else:
            product_qs = Product.objects.create(
                name = name, slug = slug, status = status,
                short_description = short_description, description = short_description, minimum_stock_quantity = minimum_stock_quantity, product_code = product_code, 
                company = company_qs, images = images, sku = sku, brand = brand_qs,
                supplier = supplier_qs, selling_tax_category = selling_tax_category_qs, buying_tax_category = buying_tax_category_qs, video_link = video_link, created_by = request_user
            )
            
        if category_qs:
            product_qs.category.add(category_qs)
            
        for product_price in product_price_list:
            buying_price = product_price.get('buying_price')
            gsheba_amount = product_price.get('gsheba_amount')
            msp = product_price.get('msp')
            mrp = product_price.get('mrp')
            corporate_price = product_price.get('corporate_price')
            b2b_price = product_price.get('b2b_price')
            advance_amount = product_price.get('advance_amount')
            
            product_price_qs = ProductPriceInfo.objects.filter(product_price_type = 'ECOMMERCE',product = product_qs ).last()
            
            if not product_price_qs:
                product_price_qs = ProductPriceInfo.objects.create(
                    product = product_qs, discount = discount_qs, promo_code = promo_code_qs, product_price_type = 'ECOMMERCE', buying_price = buying_price, gsheba_amount = gsheba_amount, msp = msp, mrp = mrp, corporate_price = corporate_price, b2b_price = b2b_price, advance_amount = advance_amount, created_by = request_user
                )
            
            product_price_qs = ProductPriceInfo.objects.filter(product_price_type = 'POINT_OF_SELL',product = product_qs ).last()
            
            if not product_price_qs:
                product_price_qs = ProductPriceInfo.objects.create(
                    product = product_qs, discount = discount_qs, promo_code = promo_code_qs, product_price_type = 'POINT_OF_SELL', buying_price = buying_price, gsheba_amount = gsheba_amount, msp = msp, mrp = mrp, corporate_price = corporate_price, b2b_price = b2b_price, advance_amount = advance_amount, created_by = request_user
                )
            
            product_price_qs = ProductPriceInfo.objects.filter(product_price_type = 'CORPORATE',product = product_qs ).last()
            
            if not product_price_qs:
                product_price_qs = ProductPriceInfo.objects.create(
                    product = product_qs, discount = discount_qs, promo_code = promo_code_qs, product_price_type = 'CORPORATE', buying_price = buying_price, gsheba_amount = gsheba_amount, msp = msp, mrp = mrp, corporate_price = corporate_price, b2b_price = b2b_price, advance_amount = advance_amount, created_by = request_user
                )
            product_price_qs = ProductPriceInfo.objects.filter(product_price_type = 'B2B',product = product_qs ).last()
            
            if not product_price_qs:
                product_price_qs = ProductPriceInfo.objects.create(
                    product = product_qs, discount = discount_qs, promo_code = promo_code_qs, product_price_type = 'B2B', buying_price = buying_price, gsheba_amount = gsheba_amount, msp = msp, mrp = mrp, corporate_price = corporate_price, b2b_price = b2b_price, advance_amount = advance_amount, is_show_in_ecommerce = is_show_in_ecommerce, is_show_in_pos = is_show_in_pos, created_by = request_user
                )
        
        # if product_qs:
            
        #     product_qs = Product.objects.all()
        #     for product_qs in product_qs:
        #         product_qs.company = company_qs
        #         product_qs.save()
        count +=1
    
    return True

def multiple_product_stock_in_create(product_list, request_user):
    created_count = 0
    product_price_list = ProductPriceInfo.objects.all()

    for product_price in product_price_list:
        # if created_count >= 50:
        #     break
        

        product_code = product_price.product.product_code
        stock_location_qs = OfficeLocation.objects.filter(office_type__in=['WAREHOUSE', 'STORE']).order_by('?').last()

        for count in range(1, 51):
            # if created_count >= 50:
            #     p

            barcode = f"{product_code}-0000{count}"

            product_stock_qs = ProductStock.objects.filter(barcode=barcode)

            if not product_stock_qs:
                ProductStock.objects.create(
                    barcode=barcode,
                    product_price_info=product_price,
                    status='ACTIVE',
                    stock_location=stock_location_qs,
                    stock_in_date=timezone.now(),
                    created_by=request_user
                )
                created_count += 1
            else:
                product_stock_qs.update(
                    barcode=barcode,
                    product_price_info=product_price,
                    status='ACTIVE',
                    stock_location=stock_location_qs,
                    stock_in_date=timezone.now(),
                    created_by=request_user
                )

                product_stock_qs.last().stock_location = stock_location_qs
                product_stock_qs.last().save()

    return True