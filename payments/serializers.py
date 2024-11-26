from rest_framework import serializers
from .models import Transaction

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = [
            'transaction_id',
            'payment_id',
            'order_id',
            'amount',
            'items',
            'status',
            'payment_method',
            'created_at',
            'customer_name',
            'customer_email',
            'customer_mobile_number',
        ]
        read_only_fields = ['transaction_id', 'created_at']
