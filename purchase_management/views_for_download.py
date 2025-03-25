from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from utils.base import render_to_pdf
from django.http import HttpResponse, HttpResponseRedirect
from .models import Purchase
from user.models import UserAccount
from .serializers import PurchaseSerializer
from datetime import datetime


class PurchasePdfDownloadView(APIView):
    def get(self, request, *args, **kwargs):
        purchase_id = self.kwargs['pk']

        purchase = Purchase.objects.select_related('initiator', 'currently_assigned_to') \
            .prefetch_related('log_entries', 'comments', 'products') \
            .get(purchase_id=purchase_id)

        serializer = PurchaseSerializer(purchase)
        current_datetime = datetime.now()

        context = {
            'purchase_id': serializer.data['purchase_id'],
            'products': serializer.data['products'],
            'initiator_name': serializer.data['initiator_name'],
            'status': serializer.data['status'],
            'currently_assigned_to_name': serializer.data['currently_assigned_to_name'],
            # 'comments': serializer.data['comments'],
            'purchase_data': serializer.data['purchase_data'],
            'purchase_payments': serializer.data['purchase_payments'],
            'created_at': serializer.data['created_at'],
            'updated_at': serializer.data['updated_at'],
            'current_datetime': current_datetime,
        }


        pdf = render_to_pdf('purchase_pdf.html', context)

        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            response['Content-Disposition'] = f'inline; filename="purchase_request_details_{current_datetime}.pdf"'
            return response
        else:
            return HttpResponse("Error generating PDF", status=500)
