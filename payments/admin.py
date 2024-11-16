""" from django.contrib import admin
from .models import Order, Transaction, Invoice

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer_name', 'total_amount', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('customer_name', 'id')
    ordering = ('-created_at',)

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'razorpay_order_id', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('razorpay_order_id', 'order__id')
    ordering = ('-created_at',)

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'invoice_url', 'generated_at')
    search_fields = ('order__id', 'invoice_url')
    ordering = ('-generated_at',)
 """


from django.contrib import admin
from .models import Order, Transaction, Invoice

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer_name', 'total_amount', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('customer_name', 'id')
    ordering = ('-created_at',)

class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'razorpay_order_id', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('razorpay_order_id', 'order__id')
    ordering = ('-created_at',)

class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'invoice_url', 'generated_at')
    search_fields = ('order__id', 'invoice_url')
    ordering = ('-generated_at',)

# Register models explicitly
admin.site.register(Order, OrderAdmin)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(Invoice, InvoiceAdmin)

