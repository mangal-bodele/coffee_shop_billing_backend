from rest_framework import serializers
from .models import Order, Transaction


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'customer_name', 'total_amount', 'status', 'created_at']


class TransactionSerializer(serializers.ModelSerializer):
    order = OrderSerializer()  # Nested serializer for order information

    class Meta:
        model = Transaction
        fields = ['id', 'order', 'razorpay_order_id', 'razorpay_payment_id', 'razorpay_signature', 'status', 'created_at']


