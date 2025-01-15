from rest_framework import serializers
from .models import Cart, CartItem
from products.models import Product

class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['id', 'cart', 'product', 'quantity']

class CartSerializer(serializers.ModelSerializer):
    # Menampilkan daftar CartItem yang terkait dengan Cart
    cart_items = CartItemSerializer(many=True, read_only=True)
    # Menampilkan total harga keranjang
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['id', 'user', 'cart_items', 'created_at', 'updated_at', 'total_price']

    def get_total_price(self, obj):
        # Menghitung total harga keranjang berdasarkan cart_item yang terkait
        total = sum(item.quantity * item.product.price for item in obj.cart_items.all())
        return total
