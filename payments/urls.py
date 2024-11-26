
from django.urls import path
from .views import CreatePaymentAPIView, VerifyPaymentAPIView,GenerateInvoiceAPIView

urlpatterns = [
    path('create-payment/', CreatePaymentAPIView.as_view(), name='create-payment'),
    path('verify-payment/', VerifyPaymentAPIView.as_view(), name='verify-payment'),
    path('generate-invoice/<str:invoice_id>/', GenerateInvoiceAPIView.as_view(), name='generate-invoice'),
]
