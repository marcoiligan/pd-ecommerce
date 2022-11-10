from django.contrib import admin
from .models import Payment, Order, OrderProduct
# Register your models here.
class OrderProductInLine(admin.TabularInline):
    model = OrderProduct
    readonly_fields = ['payment', 'user', 'product', 'variations', 'quantity', 'product_price', 'ordered']
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'full_name', 'phone', 'email', 'order_total','status']
    list_filter = ['status', 'is_ordered']
    search_fields = ['order_number', 'first_name', 'last_name', 'email']
    list_per_page = 20
    inlines = [OrderProductInLine]

class PaymentAdmin(admin.ModelAdmin):
    list_display = ['user', 'payment_id', 'amount_paid', 'status']
    search_fields = ['user','payment_id', 'status']
    list_per_page = 20

admin.site.register(Payment, PaymentAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderProduct)