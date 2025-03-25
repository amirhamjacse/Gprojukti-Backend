# serializers.py

from rest_framework import serializers
from .models import Purchase, Product, Specification, LogEntry, Comment, PurchaseData, PurchasePayment
from user.models import UserAccount

class SpecificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specification
        fields = ['key']

class ProductSerializer(serializers.ModelSerializer):
    specification = serializers.JSONField()

    class Meta:
        model = Product
        fields = ['id', 'product_name', 'specification','required_quantity']
        read_only_fields = ['id']

    def validate_specification(self, value):
    
        valid_keys = set(Specification.objects.values_list('key', flat=True))
        for key, val in value.items():
            if key not in valid_keys:
                raise serializers.ValidationError(f"Invalid specification key: {key}")
        return value

class LogEntrySerializer(serializers.ModelSerializer):
    assigned_to = serializers.SerializerMethodField()
    created_by = serializers.SerializerMethodField()
    assigned_to_phone = serializers.SerializerMethodField()

    def get_created_by(self, obj):
        if obj.created_by:
            return f"{obj.created_by.first_name} {obj.created_by.last_name}"
        return None
    def get_assigned_to(self, obj):
            if obj.assigned_to:
                return f"{obj.assigned_to.first_name} {obj.assigned_to.last_name}"
            return None
    def get_assigned_to_phone(self, obj):
        if obj.assigned_to:
            return obj.assigned_to.phone
        return None
    class Meta:
        model = LogEntry
        fields = ['id', 'date', 'action', 'status', 'assigned_to', 'comment','created_by','assigned_to_phone']
        read_only_fields = ['id', 'date', 'assigned_to','assigned_to_phone']

class CommentSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.first_name', read_only=True)
    user_email = serializers.EmailField(source='user.email', read_only=True) 

    class Meta:
        model = Comment
        fields = ['id', 'date_time', 'text', 'user_name', 'user_email']
        read_only_fields = ['id', 'date_time', 'user_name', 'user_email']

class PurchaseDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseData
        fields = [
            'id',
            'product',
            'required_qty',
            'vendor',
            'previous_unit_price',
            'quoted_price',
            'required_budget',
            'is_approved',
            'is_rejected',
        ]
        read_only_fields = ['id']

class PurchasePaymentSerializer(serializers.ModelSerializer):
    paid_to_name  = serializers.SerializerMethodField(read_only=True)
    paid_by_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = PurchasePayment
        fields = ['id',  'amount', 'payment_date', 'payment_mode','note','created_at','transaction_id','paid_to_name','paid_by_name']
        read_only_fields = ['id','paid_to_name','paid_by_name','created_at','purchase']

    def get_paid_to_name(self, obj):
        return str(obj.paid_to) if str(obj.paid_to) else None
    def get_paid_by_name(self, obj):
        return str(obj.paid_by) if str(obj.paid_by) else None

class PurchaseSerializer(serializers.ModelSerializer):
    initiator_name = serializers.SerializerMethodField(read_only=True)
    currently_assigned_to_name = serializers.SerializerMethodField(read_only=True)
    log_entries = LogEntrySerializer(many=True, read_only=True)
    purchase_payments = PurchasePaymentSerializer(many=True, read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    products = ProductSerializer(many=True)
    purchase_data = serializers.SerializerMethodField()  # Custom method field for filtering

    class Meta:
        model = Purchase
        fields = [
            'purchase_id', 'products', 'initiator_name', 'status',
            'currently_assigned_to_name', 'log_entries', 'comments','currently_assigned_to_id',
            'created_at', 'updated_at', 'purchase_data', 'purchase_payments'
        ]
        read_only_fields = ['initiator_name', 'currently_assigned_to_name', 'currently_assigned_to_id','log_entries', 'comments', 'created_at', 'updated_at', 'purchase_data', 'purchase_payments']

    def get_initiator_name(self, obj):
        return str(obj.initiator) if str(obj.initiator) else None

    def get_currently_assigned_to_name(self, obj):
        return str(obj.currently_assigned_to) if str(obj.currently_assigned_to) else None

    def get_purchase_data(self, obj):
        # Retrieve `is_approved` from the serializer context
        is_approved = self.context.get("is_approved")
        if is_approved is not None:
            # Filter purchase_data based on the `is_approved` flag
            return PurchaseDataSerializer(obj.purchase_data.filter(is_approved=is_approved), many=True).data
        return PurchaseDataSerializer(obj.purchase_data.all(), many=True).data

    def create(self, validated_data):
        products_data = validated_data.pop('products')
        purchase = Purchase.objects.create(**validated_data)
        for product_data in products_data:
            Product.objects.create(purchase=purchase, **product_data)
        return purchase

    def update(self, instance, validated_data):
        products_data = validated_data.pop('products', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if products_data:
            # Remove existing products and add updated products
            instance.products.all().delete()
            for product_data in products_data:
                Product.objects.create(purchase=instance, **product_data)
        return instance

from rest_framework import serializers

class CSVReadSerializer(serializers.Serializer):
    file = serializers.FileField()

    def validate_file(self, value):
        """
        Validate that the uploaded file is a CSV and within size limits.
        """
        if not value.name.endswith('.csv'):
            raise serializers.ValidationError("Only CSV files are supported.")
        if value.size > 5 * 1024 * 1024:  # 5MB limit
            raise serializers.ValidationError("File size exceeds 5MB limit.")
        return value