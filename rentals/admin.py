from django.contrib import admin
from .models import Cart, Order, Shipping, OrderItem

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'quantity', 'total_price')
    search_fields = ('user__username', 'product__name')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total_price', 'borrow_date', 'return_deadline', 'status', 'created_at')
    list_filter = ('status', 'borrow_date', 'return_deadline')
    search_fields = ('user__username',)

@admin.register(Shipping)
class ShippingAdmin(admin.ModelAdmin):
    list_display = ('order', 'user_name', 'address', 'postal_code', 'phone_number')
    search_fields = ('user_name', 'order__id')

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'total_price')
    search_fields = ('order__id', 'product__name')
