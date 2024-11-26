from django.db import models

class Transaction(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
        ('Failed', 'Failed'),
        ('Refunded', 'Refunded'),
        ('Cancelled', 'Cancelled'),
    ]

    PAYMENT_METHOD_CHOICES = [
        ('Card', 'Card'),
        ('UPI', 'UPI'),
        ('Cash', 'Cash'),
    ]

    transaction_id = models.CharField(max_length=100, unique=True)
    payment_id = models.CharField(max_length=100, unique=True, blank=True, null=True)
    order_id = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    items = models.JSONField()  # Stores cart items in JSON format
    status = models.CharField(
        max_length=50,
        choices=STATUS_CHOICES,
        default="Pending"
    )
    payment_method = models.CharField(
        max_length=50,
        choices=PAYMENT_METHOD_CHOICES,
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    # Customer details
    customer_name = models.CharField(max_length=255, blank=True, null=True)
    customer_email = models.EmailField(blank=True, null=True)
    customer_mobile_number = models.CharField(max_length=15, blank=True, null=True)  # Customer's mobile number

    def __str__(self):
        return f"Transaction {self.transaction_id} - {self.status}"
