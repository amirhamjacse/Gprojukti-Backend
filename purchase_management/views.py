from django.utils import timezone
from rest_framework import generics, permissions, status, exceptions
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Purchase, LogEntry, Comment, Product,Specification,PurchaseData,PurchasePayment
from user.models import UserAccount
from .serializers import PurchaseSerializer, CommentSerializer, ProductSerializer,SpecificationSerializer,PurchaseDataSerializer,PurchasePaymentSerializer
from django.shortcuts import get_object_or_404
from django.db import transaction
import csv
import io
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from .serializers import CSVReadSerializer
from .models import StockModel
from rest_framework.views import APIView
from utils.response_wrapper import ResponseWrapper
class SpecificationListCreateAPIView(generics.ListCreateAPIView):
    """
    GET: List all specifications.
    POST: Create a new specification.
    """
    queryset = Specification.objects.all()
    serializer_class = SpecificationSerializer
    permission_classes = [permissions.IsAuthenticated]  

class SpecificationRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET: Retrieve a specific specification.
    PUT: Update a specific specification.
    DELETE: Delete a specific specification.
    """
    queryset = Specification.objects.all()
    serializer_class = SpecificationSerializer
    permission_classes = [permissions.IsAuthenticated]  

# class PurchaseListCreateAPIView(generics.ListCreateAPIView):
#     queryset = Purchase.objects.select_related('initiator', 'currently_assigned_to').prefetch_related('log_entries', 'comments', 'products').all()
#     serializer_class = PurchaseSerializer
#     permission_classes = [IsAuthenticated]

#     @transaction.atomic
#     def perform_create(self, serializer):
#         currently_assigned_to_id = self.request.data.get("currently_assigned_to")
#         currently_assigned_to_user = UserAccount.objects.filter(id=currently_assigned_to_id).first()
#         print(currently_assigned_to_user,currently_assigned_to_id)
#         purchase = serializer.save(
#             initiator=self.request.user,
#             currently_assigned_to=currently_assigned_to_user
#         )
#         # Log creation
#         LogEntry.objects.create(
#             purchase=purchase,
#             action="created",
#             status=purchase.status,
#             assigned_to=currently_assigned_to_user,
#             created_by=self.request.user
#         )


class PurchaseListCreateAPIView(generics.ListCreateAPIView):
    queryset = Purchase.objects.select_related(
        'initiator', 'currently_assigned_to'
    ).prefetch_related(
        'log_entries', 'comments', 'products'
    ).order_by('-purchase_id')
    serializer_class = PurchaseSerializer
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def perform_create(self, serializer):
        currently_assigned_to_id = self.request.data.get("currently_assigned_to")
        currently_assigned_to_user = UserAccount.objects.filter(id=currently_assigned_to_id).first()
        print(currently_assigned_to_user, currently_assigned_to_id)
        
        if not currently_assigned_to_user:
            raise exceptions.ValidationError({"currently_assigned_to": "User does not exist."})

        purchase = serializer.save(
            initiator=self.request.user,
            currently_assigned_to=currently_assigned_to_user
        )
        # Log creation
        LogEntry.objects.create(
            purchase=purchase,
            action="created",
            status=purchase.status,
            assigned_to=currently_assigned_to_user,
            created_by=self.request.user
        )

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        # Apply pagination
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            paginated_data = self.get_paginated_response(serializer.data).data
            return ResponseWrapper(
                data=paginated_data,
                msg="Purchases retrieved successfully.",
                status=status.HTTP_200_OK
            )

        serializer = self.get_serializer(queryset, many=True)
        return ResponseWrapper(
            data=serializer.data,
            msg="Purchases retrieved successfully.",
            status=status.HTTP_200_OK
        )

class PurchaseDetailAPIView(generics.RetrieveUpdateAPIView):
    queryset = Purchase.objects.select_related('initiator', 'currently_assigned_to').prefetch_related('log_entries', 'comments', 'products').all()
    serializer_class = PurchaseSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        is_approved = self.request.query_params.get('is_approved')
        if is_approved is not None:
            context["is_approved"] = is_approved.lower() == 'true'
        return context

    @transaction.atomic
    def perform_update(self, serializer):
        currently_assigned_to_id = self.request.data.get("currently_assigned_to")
        currently_assigned_to_user = UserAccount.objects.filter(id=currently_assigned_to_id).first()
        purchase = serializer.save(
            initiator=self.request.user,
            currently_assigned_to=currently_assigned_to_user
        )
        # Log update
        LogEntry.objects.create(
            purchase=purchase,
            action="updated",
            status=purchase.status,
            assigned_to=currently_assigned_to_user,
            created_by=self.request.user
        )
class AddCommentAPIView(generics.CreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request, purchase_id, *args, **kwargs):
        purchase = get_object_or_404(Purchase, pk=purchase_id)
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            comment = serializer.save(purchase=purchase, user=request.user)
            # Log the comment
            LogEntry.objects.create(
                purchase=purchase,
                action="commented",
                status=purchase.status,
                assigned_to=purchase.currently_assigned_to,
                comment=comment.text,
                created_by=self.request.user
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from rest_framework import serializers

class PurchaseDataListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = PurchaseDataSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        purchase_id = self.kwargs.get('purchase_id')
        return PurchaseData.objects.filter(purchase__purchase_id=purchase_id)

    @transaction.atomic
    def perform_create(self, serializer):
        """
        Handle creation of multiple PurchaseData entries in a single request.
        """
        purchase_id = self.kwargs.get('purchase_id')
        purchase = get_object_or_404(Purchase, purchase_id=purchase_id)
        
        payload = self.request.data  # Expecting a list of dictionaries
        if not isinstance(payload, list):
            raise serializers.ValidationError({"error": "Payload must be a list of objects."})
        
        created_entries = []
        for data in payload:
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            purchase_data = serializer.save(purchase=purchase)
            created_entries.append(purchase_data)

            # Log each entry
            LogEntry.objects.create(
                purchase=purchase,
                action="purchase_data_created",
                status=purchase.status,
                assigned_to=purchase.currently_assigned_to,
                comment=f"PurchaseData {purchase_data.id} created.",
                created_by=self.request.user
            )
        
        return created_entries  # Returning the created entries

    def create(self, request, *args, **kwargs):
        """
        Override the create method to handle custom response for multiple objects.
        """
        with transaction.atomic():
            created_entries = self.perform_create(None)
            serializer = self.get_serializer(created_entries, many=True)
            return Response(serializer.data, status=status.HTTP_201_CREATED)



class PurchaseDataDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PurchaseDataSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        purchase_id = self.kwargs.get('purchase_id')
        return PurchaseData.objects.filter(purchase__purchase_id=purchase_id)
    
    def perform_update(self, serializer):
        purchase_data = serializer.save()
        purchase = purchase_data.purchase
   
        LogEntry.objects.create(
       
            log_json=[{
                 "purchase": purchase,
                "date": timezone.now().isoformat(),
                "action": "updated_purchase_data",
                "status": purchase.status,
                "assigned_to": str(purchase.currently_assigned_to) if purchase.currently_assigned_to else None,
                "purchase_data": PurchaseDataSerializer(purchase_data).data
            }]
        )
    
    def perform_destroy(self, instance):
        purchase = instance.purchase
      
        LogEntry.objects.create(
         
            log_json=[{
                "purchase": purchase,
                "date": timezone.now().isoformat(),
                "action": "deleted_purchase_data",
                "status": purchase.status,
                "assigned_to": str(purchase.currently_assigned_to) if purchase.currently_assigned_to else None,
                "purchase_data": PurchaseDataSerializer(instance).data
            }]
        )
        instance.delete()



class PurchasePaymentAPIView(generics.ListCreateAPIView):
    """
    GET: List all PurchasePayment entries for a specific Purchase.
    POST: Create a new PurchasePayment entry for a specific Purchase.
    """
    serializer_class = PurchasePaymentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Retrieves all PurchasePayment instances related to the specified Purchase.
        """
        purchase_id = self.kwargs.get('purchase_id')
        return PurchasePayment.objects.filter(purchase__purchase_id=purchase_id)

    @transaction.atomic
    def perform_create(self, serializer):
        """
        Creates a PurchasePayment instance and logs the creation in LogEntry.
        Automatically sets 'purchase', 'paid_to', and 'paid_by' fields.
        """
        purchase_id = self.kwargs.get('purchase_id')
        purchase = get_object_or_404(Purchase, purchase_id=purchase_id)

       
        paid_to_user = purchase.currently_assigned_to

        paid_by_user = self.request.user


        purchase_payment = serializer.save(
            purchase=purchase,
            paid_to=paid_to_user,
            paid_by=paid_by_user
        )

        # Log the creation of PurchasePayment
        LogEntry.objects.create(
            purchase=purchase,
            action="purchase_payment_created",  # Updated action
            status=purchase.status,
            assigned_to=paid_to_user,
            comment=f"PurchasePayment {purchase_payment.id} of amount {purchase_payment.amount} created.",
            created_by=paid_by_user
        )




class ApprovePurchaseDataAPIView(APIView):
    def post(self, request, purchase_data_id):
        try:
            purchase_data = PurchaseData.objects.get(id=purchase_data_id)
            purchase_data.is_approved = True
            purchase_data.save()
            serializer = PurchaseDataSerializer(purchase_data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except PurchaseData.DoesNotExist:
            return Response({"error": "PurchaseData not found"}, status=status.HTTP_404_NOT_FOUND)

class ApprovedPurchaseDataListAPIView(generics.ListAPIView):
    serializer_class = PurchaseDataSerializer

    def get_queryset(self):
        purchase_id = self.kwargs['purchase_id']
        return PurchaseData.objects.filter(purchase__purchase_id=purchase_id, is_approved=True)


class ReadFirstColumnAPIView(generics.GenericAPIView):
    """
    POST: Upload a CSV file and store the data in the StockModel.
    """
    serializer_class = CSVReadSerializer
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            csv_file = serializer.validated_data['file']

            # Decode the uploaded file
            try:
                decoded_file = csv_file.read().decode('utf-8')
            except UnicodeDecodeError:
                return Response(
                    {"error": "Invalid file encoding. Please upload a UTF-8 encoded CSV file."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Use StringIO to read the CSV data
            io_string = io.StringIO(decoded_file)
            reader = csv.DictReader(io_string)  # Use DictReader to get column names

            errors = []
            line_number = 0  # To track line numbers for error reporting

            for row in reader:
                line_number += 1
                try:
                    # Extract fields from the row
                    quantity = int(row['quantity'])
                    pos_product_code = row['pos_product_code'].strip()
                    store_name = row['store_name'].strip()

                    # Check if the entry exists
                    stock_entry, created = StockModel.objects.get_or_create(
                        pos_product_code=pos_product_code,
                        store_name=store_name,
                        defaults={'quantity': quantity}
                    )

                    if not created:
                        # If the entry exists, add the new quantity to the existing quantity
                        stock_entry.quantity += quantity
                        stock_entry.save()

                except Exception as e:
                    errors.append({
                        'line': line_number,
                        'error': str(e)
                    })

            response_data = {
                "message": "CSV data uploaded and quantities updated successfully."
            }

            if errors:
                response_data["errors"] = errors
                return Response(response_data, status=status.HTTP_207_MULTI_STATUS)  # 207 indicates multi-status

            return Response(response_data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)