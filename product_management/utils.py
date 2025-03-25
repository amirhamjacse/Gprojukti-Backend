from product_management.models.product import ProductStockLog
from product_management.serializers.product import ProductStockSerializer


def barcode_status_log(product_stock_qs, previous_status, previous_status_display, current_status, remarks, is_active, stock_in_date, request_user):
    
    product_stock_serializer_data = ProductStockSerializer(product_stock_qs).data
                
    current_status_display  = product_stock_serializer_data.get('status_display')
    stock_status_change_by_info  = product_stock_serializer_data.get('created_by')
    
    stock_in_age  = product_stock_serializer_data.get('stock_in_age')
    
    stock_location_info  = product_stock_serializer_data.get('stock_location')
    
    product_stock_log_qs = ProductStockLog.objects.create(
                product_stock = product_stock_qs, 
                previous_status = previous_status,
                previous_status_display = previous_status_display,
                current_status = current_status,
                current_status_display = current_status_display,
                remarks = remarks,
                is_active = is_active,
                stock_status_change_by_info = stock_status_change_by_info,
                stock_in_date = stock_in_date,
                stock_in_age = stock_in_age,
                stock_location_info = stock_location_info,
                
                created_by = request_user,
                updated_by = request_user,
                created_at = stock_in_date,
            )
    
    
    return product_stock_log_qs