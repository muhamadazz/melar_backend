from django.contrib import admin
from .models import Cart, Order, Shipping, OrderItem

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'quantity', 'total_price')
    search_fields = ('user__username', 'product__name')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'renter', 'phone_renter', 'provider', 'phone_provider', 'product', 'total_price', 'status', 'borrow_date', 'return_deadline', 'created_at')
    list_filter = ('status', 'borrow_date', 'return_deadline', 'created_at')
    search_fields = ('renter__username', 'phone_renter', 'provider', 'phone_provider', 'product__name', 'status')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at', 'phone_renter', 'provider', 'phone_provider')

    def save_model(self, request, obj, form, change):
        if not obj.phone_renter and obj.renter:
            obj.phone_renter = obj.renter.phone_number
        if obj.product and obj.product.shop and obj.product.shop.user:
            obj.provider = obj.product.shop.user.full_name
            obj.phone_provider = obj.product.shop.user.phone_number
        super().save_model(request, obj, form, change)

@admin.register(Shipping)
class ShippingAdmin(admin.ModelAdmin):
    list_display = ('order', 'user_name', 'address', 'postal_code', 'phone_number')
    search_fields = ('user_name', 'order__id')

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'total_price')
    search_fields = ('order__id', 'product__name')
