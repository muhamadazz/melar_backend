from rest_framework import serializers
from .models import Cart, Order, Shipping, OrderItem
from shops.models import Product

class CartSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'user', 'product', 'product_name', 'quantity', 'total_price']
        read_only_fields = ['user', 'total_price', 'product_name']

class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_owner = serializers.CharField(source='product.shop.user.username', read_only=True)  # Ambil dari shop -> user
    phone_number = serializers.CharField(source='product.shop.user.phone_number', read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_name','phone_number','product_owner', 'quantity', 'total_price']
        read_only_fields = ['product_name', 'product_owner', 'phone_number']


class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'order_items', 'total_price', 'borrow_date', 'return_deadline', 'status', 'created_at', 'updated_at']
        read_only_fields = ['user', 'status', 'created_at', 'updated_at']

    def create(self, validated_data):
        user = self.context['request'].user
        order_items_data = validated_data.pop('order_items', [])

        order = Order.objects.create(user=user, **validated_data)

        for item_data in order_items_data:
            OrderItem.objects.create(order=order, **item_data)

        return order

class ShippingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shipping
        fields = ['id', 'order', 'address', 'postal_code', 'phone_number', 'user_name']

    def validate_phone_number(self, value):
        if not value.isdigit() or len(value) < 10:
            raise serializers.ValidationError("Phone number must be at least 10 digits.")
        return value

    def validate_postal_code(self, value):
        if not value.isdigit() or len(value) != 5:
            raise serializers.ValidationError("Postal code must be exactly 5 digits.")
        return value
