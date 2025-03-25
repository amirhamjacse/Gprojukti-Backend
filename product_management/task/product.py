# tasks.py

from celery import shared_task
from rest_framework.response import Response
from rest_framework.views import APIView
import asyncio
from product_management.models.product import *
from product_management.serializers.product import *

@shared_task
def process_product_stock_data():
    print(f"Perform your processing here without relying on instance methods")
    # Perform your processing here without relying on instance methods
    # For example:
    # queryset = ProductStock.objects.all()
    # serializer = ProductStockSerializer(queryset, many=True)
    # serialized_data = serializer.data
    # # Process the serialized data as needed
    processed_data = []
    # for item in serialized_data:
    #     processed_item = {
    #         'id': item['id'],
    #         'barcode': item['barcode'],
    #         # Add more processing here ifF needed
    #     }
    #     processed_data.append(processed_item)
    return processed_data