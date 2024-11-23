from django.urls import path
from .views import CreatePaymentAPIView,VerifyPaymentAPIView,InvoiceView

urlpatterns = [
    path('create-payment/', CreatePaymentAPIView.as_view(), name='create-payment'),
    path('verify-payment/', VerifyPaymentAPIView.as_view(), name='verify-payment'),
    path('invoice/<str:transaction_id>/', InvoiceView.as_view(), name='generate_invoice'),

]
