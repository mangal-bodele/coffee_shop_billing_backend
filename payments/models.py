import uuid
from django.db import models


class Order(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,  # Automatically generates a unique UUID
        editable=False
    )
    customer_name = models.CharField(max_length=255)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=50,
        choices=[('pending', 'Pending'), ('paid', 'Paid')],
        default='pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} - {self.customer_name}"

    class Meta:
        db_table = 'order'


class Transaction(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='transactions')
    razorpay_order_id = models.CharField(max_length=255)
    razorpay_payment_id = models.CharField(max_length=255, blank=True, null=True)
    razorpay_signature = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(
        max_length=50,
        choices=[('pending', 'Pending'), ('verified', 'Verified')],
        default='pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Transaction for Order {self.order.id}"

    def clean(self):
        # Ensure razorpay_payment_id and razorpay_signature are set when status is 'verified'
        if self.status == 'verified' and not (self.razorpay_payment_id and self.razorpay_signature):
            raise models.ValidationError('Payment ID and Signature must be provided when verified.')

    class Meta:
        db_table = 'transaction'





