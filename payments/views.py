from rest_framework.generics import GenericAPIView
from django.conf import settings
import razorpay
import hashlib
import hmac

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Order, Transaction


# Razorpay client initialization
razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))


class CreatePaymentAPIView(GenericAPIView):
    """
    API endpoint to create a Razorpay order for payment.
    """

    def post(self, request, *args, **kwargs):
        """
        Handles the creation of a Razorpay order.
        """
        try:
            # Extract cart items and total amount from the request
            cart_items = request.data.get("cart_items", [])
            total_amount = request.data.get("total_amount")

            if not cart_items or not total_amount:
                return Response(
                    {"error": "Invalid cart items or total amount."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Create Razorpay order
            razorpay_order = razorpay_client.order.create(
                {
                    "amount": int(total_amount * 100),  # Convert amount to paise
                    "currency": "INR",
                    "payment_capture": 1,  # Auto capture
                }
            )

            # Return order details to the frontend
            return Response(
                {
                    "orderId": razorpay_order.get("id"),
                    "razorpayKey": settings.RAZORPAY_KEY_ID,
                    "currency": razorpay_order.get("currency"),
                },
                status=status.HTTP_201_CREATED,
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class VerifyPaymentAPIView(GenericAPIView):
    """
    API endpoint to verify Razorpay payment signatures.
    """

    def post(self, request, *args, **kwargs):
        """
        Verifies the payment details and signature sent by Razorpay.
        """
        try:
            # Extract payment details from the request
            razorpay_payment_id = request.data.get("payment_id")
            razorpay_order_id = request.data.get("order_id")
            razorpay_signature = request.data.get("signature")

            if not (razorpay_payment_id and razorpay_order_id and razorpay_signature):
                return Response(
                    {"error": "Missing payment details."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Generate signature and verify
            generated_signature = hmac.new(
                settings.RAZORPAY_KEY_SECRET.encode("utf-8"),
                f"{razorpay_order_id}|{razorpay_payment_id}".encode("utf-8"),
                hashlib.sha256,
            ).hexdigest()

            if generated_signature != razorpay_signature:
                return Response(
                    {"error": "Invalid payment signature."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Payment verified successfully
            # Save transaction details to the database (optional)
            transaction_id = razorpay_payment_id  # Use payment_id as transaction_id

            return Response(
                {"message": "Payment successful.", "transaction_id": transaction_id},
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )



from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Order, Transaction

class InvoiceView(APIView):
    def get(self, request, transaction_id):
        """
        Generate invoice based on Razorpay Transaction ID.
        """
        try:
            # Fetch the transaction using the transaction_id
            transaction = Transaction.objects.get(id=transaction_id)
            order = transaction.order  # Fetch the associated order

            # Prepare invoice data
            data = {
                "invoice_type": "Transaction",
                "razorpay_order_id": transaction.razorpay_order_id,
                "razorpay_payment_id": transaction.razorpay_payment_id,
                "status": transaction.status,
                "created_at": transaction.created_at,
                "order_details": {
                    "order_id": str(order.id),
                    "customer_name": order.customer_name,
                    "total_amount": str(order.total_amount),
                    "status": order.status,
                    "created_at": order.created_at,
                },
            }
            return Response(data, status=status.HTTP_200_OK)

        except Transaction.DoesNotExist:
            return Response({"error": "Transaction not found"}, status=status.HTTP_404_NOT_FOUND)
