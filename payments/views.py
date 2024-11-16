from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from django.http import HttpResponse
import pdfkit  # For generating PDF invoices (ensure wkhtmltopdf is installed)
import razorpay
import hashlib
import hmac
from .models import Order, Transaction, Invoice
from rest_framework.views import APIView
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from reportlab.pdfgen import canvas
from .models import Transaction, Order
from rest_framework import status
from rest_framework.generics import GenericAPIView


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




class GenerateInvoiceView(GenericAPIView):
    """
    View to generate an invoice for a specific transaction and order.
    Inherits from DRF's GenericAPIView.
    """
    def get(self, request, transaction_id, *args, **kwargs):
        # Fetch the transaction and related order using transaction_id
        transaction = get_object_or_404(Transaction, id=transaction_id)
        order = get_object_or_404(Order, id=transaction.order.id)

        # Create a response for PDF
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="invoice_{transaction_id}.pdf"'

        # Generate PDF
        p = canvas.Canvas(response)

        # Add title
        p.drawString(100, 800, "Invoice")

        # Add transaction and order details
        p.drawString(100, 780, f"Transaction ID: {transaction.razorpay_order_id}")
        p.drawString(100, 760, f"Date: {transaction.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
        p.drawString(100, 740, f"Customer: {order.customer_name}")
        p.drawString(100, 720, f"Total Amount: ₹{order.total_amount}")

        # Order Details (assuming order has related order items)
        y_position = 700
        for item in order.orderitem_set.all():
            p.drawString(100, y_position, f"{item.product.name} - ₹{item.price} x {item.quantity}")
            y_position -= 20

        p.drawString(100, y_position - 20, f"Total: ₹{order.total_amount}")
        p.showPage()
        p.save()

        return response

