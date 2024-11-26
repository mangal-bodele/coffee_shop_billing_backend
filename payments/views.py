import datetime
import hmac
import hashlib
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import GenericAPIView
import razorpay
from django.conf import settings


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


class GenerateInvoiceAPIView(GenericAPIView):
    """
    API endpoint to generate an invoice for a successful payment.
    """

    def get(self, request, *args, **kwargs):
        transaction_id = request.query_params.get('transaction_id')
        if not transaction_id:
            return Response({"error": "Transaction ID missing"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Fetch payment details from the database using transaction_id
        # Example: payment = Payment.objects.get(transaction_id=transaction_id)

        # Generate invoice logic
        invoice_data = {
            'transaction_id': transaction_id,
            'amount': 1000,  # Example amount
            'date': datetime.now().strftime('%Y-%m-%d'),
            'items': [{'name': 'Item 1', 'price': 500}, {'name': 'Item 2', 'price': 500}]
        }
        
        # Return invoice data or a file (e.g., PDF)
        return Response({"invoice": invoice_data}, status=status.HTTP_200_OK)

