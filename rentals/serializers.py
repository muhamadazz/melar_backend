from rest_framework import serializers
from .models import Cart, Order, Shipping, OrderItem
from shops.models import Product


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['id', 'user', 'product', 'quantity', 'total_price']
        read_only_fields = ['user', 'total_price']

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity', 'total_price']

class OrderSerializer(serializers.ModelSerializer):
    # Ganti cart_items dengan order_items karena Cart sudah tidak berhubungan langsung dengan Order lagi
    order_items = OrderItemSerializer(many=True, read_only=True)  
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'order_items', 'total_price', 'borrow_date', 'return_deadline', 'status', 'created_at', 'updated_at']
        read_only_fields = ['user', 'status', 'created_at', 'updated_at']

    def create(self, validated_data):
        # Mendapatkan user dari request (dari context)
        user = self.context['request'].user  # Mendapatkan user yang sedang login
        
        # Cart items tidak perlu diambil dari validated_data, karena sudah ditangani di viewset
        # Order items akan ditangani di viewset saat checkout
        cart_items = validated_data.get('cart_items', [])

        # Total price sudah dihitung di viewset, kita tidak perlu menghitungnya di sini lagi
        total_price = validated_data.get('total_price', 0)

        # Membuat order baru dengan total_price yang sudah dihitung
        order = Order.objects.create(
            user=user,  # Menetapkan user yang sedang login
            total_price=total_price,
            **validated_data
        )

        # Order items akan ditambahkan oleh viewset ketika checkout, jadi tidak perlu di sini
        order.save()

        return order


class ShippingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shipping
        fields = ['id', 'order', 'address', 'postal_code', 'phone_number', 'user_name']
