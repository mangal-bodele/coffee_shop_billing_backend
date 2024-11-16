from django.urls import path
from .views import CreatePaymentAPIView,VerifyPaymentAPIView,GenerateInvoiceView

urlpatterns = [
    path('create-payment/', CreatePaymentAPIView.as_view(), name='create-payment'),
    path('verify-payment/', VerifyPaymentAPIView.as_view(), name='verify-payment'),
    path('invoice/<uuid:transaction_id>/', GenerateInvoiceView.as_view(), name='generate-invoice'),

]






