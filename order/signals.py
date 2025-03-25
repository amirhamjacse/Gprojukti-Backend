# import channels.layers
# from asgiref.sync import async_to_sync, sync_to_async
# from channels.db import database_sync_to_async
# from channels.generic.websocket import JsonWebsocketConsumer
# from django.conf import settings
# from django.dispatch import Signal, receiver
# from django.template.loader import render_to_string
# from django.utils import timezone
# from utils.print_node import print_node
# from weasyprint import CSS, HTML

# from order.models import Order
# from order.serializers import *
# from django_q.tasks import async_task


# order_done_signal = Signal(
#     providing_args=["qs", "data", "state"])

# kitchen_items_print_signal = Signal(
#     providing_args=["qs"])

# @receiver(order_done_signal)
# def socket_fire_on_order_change_signals(sender,   restaurant_id, order_id=None, qs=None, data=None, state='data_only', **kwargs):
#     """
#     signal reciever for dashboard update and call websocket connections

#     Parameters
#     ----------
#     sender : signal sender ref

#     order_qs : queryset
#         Order
#     table_qs : queryset
#         Table
#     state : str
#         [data_only]
#     """
#     if settings.TURN_OFF_SIGNAL:
#         return
#     # print('---------------------------------------------------------------------------------------------------------------')
#     # print("FIRING Signals")
#     # print('---------------------------------------------------------------------------------------------------------------')
#     async_task('restaurant.tasks.socket_fire_task_on_order_crud',
#                restaurant_id, order_id, state, data)
#     # socket_fire_task_on_order_crud(restaurant_id, order_id, state, data)